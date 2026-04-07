from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import EmailStr, TypeAdapter, ValidationError
from sqlalchemy.orm import Session

from config.settings import get_settings
from db.models import User, UserSession
from db.session import get_db
from delivery.email import send_magic_link

_email_validator = TypeAdapter(EmailStr)

router = APIRouter(tags=["auth"])
settings = get_settings()

TOPIC_CARDS = [
    "LLM infrastructure", "AI agents", "MLOps", "Prompt engineering",
    "Frontend development", "Systems design", "Data engineering",
    "AI for productivity", "Open-source models", "Evaluation and testing",
]


@router.post("/signup")
async def signup(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Handles both HTML form POST and JSON POST.
    Upserts user, generates magic link token, sends via Resend (or logs in dry-run).
    """
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        data = await request.json()
        email = data.get("email", "")
        name = data.get("name")
        interests = data.get("interests", [])
        delivery_time = data.get("delivery_time")
    else:
        form = await request.form()
        email = str(form.get("email", "")).strip()
        name = str(form.get("name", "")).strip() or None
        interests = [v.strip() for v in form.getlist("interests") if str(v).strip()]
        delivery_time = str(form.get("delivery_time", "")).strip() or None

    if not email:
        return HTMLResponse("Email is required.", status_code=400)

    try:
        email = _email_validator.validate_python(email)
    except ValidationError:
        return HTMLResponse("Invalid email address.", status_code=400)

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=name, interests=interests)
        db.add(user)
    else:
        if name:
            user.name = name
        if interests:
            user.interests = interests

    if delivery_time:
        user.delivery_time = delivery_time

    user.magic_link_token = token_urlsafe(32)
    user.magic_link_expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.magic_link_ttl_minutes
    )
    db.commit()

    verify_url = f"{settings.app_url}/api/auth/verify?token={user.magic_link_token}"
    send_magic_link(user.email, verify_url)

    if "application/json" in content_type:
        return {"message": "Check your email for a sign-in link."}

    # In dev, show the link directly so you can click it without email
    dev_hint = ""
    if not settings.is_production:
        dev_hint = (
            f"<p style='margin-top:1rem;font-size:0.875rem;color:#6b7280;'>"
            f"Dev link: <a href='{verify_url}'>{verify_url}</a></p>"
        )

    return HTMLResponse(
        "<html><body style='font-family:system-ui;"
        "max-width:480px;margin:4rem auto;padding:0 1rem'>"
        f"<h2>Check your email</h2>"
        f"<p>We sent a sign-in link to <strong>{email}</strong>.</p>"
        f"{dev_hint}"
        f"</body></html>"
    )


@router.get("/auth/verify")
def verify_magic_link(token: str, db: Session = Depends(get_db)):
    """Validate magic link token, create session cookie, redirect to /feed."""
    user = (
        db.query(User)
        .filter(
            User.magic_link_token == token,
            User.magic_link_expires_at > datetime.now(UTC),
        )
        .first()
    )
    if not user:
        return HTMLResponse("Invalid or expired link. Please sign up again.", status_code=401)

    session = UserSession(
        user_id=user.id,
        token=token_urlsafe(32),
        expires_at=datetime.now(UTC) + timedelta(days=settings.session_ttl_days),
    )
    user.magic_link_token = None
    user.magic_link_expires_at = None
    db.add(session)
    db.commit()

    response = RedirectResponse(url="/feed", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="session_token",
        value=session.token,
        httponly=True,
        samesite="lax",
        secure=settings.is_production,
        max_age=settings.session_ttl_days * 24 * 60 * 60,
    )
    return response
