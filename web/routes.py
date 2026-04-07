from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.deps import get_current_user
from db.models import ContentItem, Interaction, User
from db.session import get_db
from scoring.ranker import fetch_candidates, rank_items_for_user

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="web/templates")

TOPIC_CARDS = [
    # AI & Machine Learning
    "Foundation models & LLMs", "Open-source AI", "Multimodal AI",
    "AI research & papers", "Evaluation & benchmarks",
    "AI agents & automation", "AI infrastructure & compute", "Training & fine-tuning",
    "MLOps & deployment", "Data & knowledge", "AI tools & productivity",
    "Creative AI", "AI in science", "Robotics & embodied AI",
    "AI safety & alignment", "AI policy & regulation", "AI economics & society",
    "AI in business & industry", "Prompt engineering & AI UX", "AI hardware & chips",
    # General Interest
    "Software engineering", "Cybersecurity", "Cloud computing",
    "Space & astronomy", "Biotech & life sciences", "Climate & environment",
    "Startups & venture capital", "Career & professional growth",
    "Personal finance & investing", "Economics & markets",
    "Geopolitics & international affairs", "Health & wellness",
    "Education & learning", "Design & creativity", "Science & research",
]


@router.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse(
        request, "landing.html", {"topic_cards": TOPIC_CARDS}
    )


@router.get("/feed", response_class=HTMLResponse)
def feed(
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items = fetch_candidates(db)
    ranked = rank_items_for_user(items, user)
    return templates.TemplateResponse(
        request, "feed.html", {"user": user, "items": ranked[:20]}
    )


@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        request, "settings.html", {"user": user, "topic_cards": TOPIC_CARDS}
    )


@router.post("/settings")
async def update_settings(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    delivery_time: str | None = Form(default=None),
    interests: list[str] = Form(default=[]),
):
    if delivery_time:
        user.delivery_time = delivery_time
    user.interests = interests
    db.add(user)
    db.commit()
    return RedirectResponse(url="/settings", status_code=303)


@router.get("/click/{content_id}")
def track_click(
    content_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Track a click from the web feed (requires auth session)."""
    item = db.query(ContentItem).filter(ContentItem.id == content_id).first()
    if not item:
        return RedirectResponse(url="/feed", status_code=303)

    db.add(Interaction(
        user_id=user.id,
        content_id=item.id,
        action="click",
        source_surface="web",
    ))
    db.commit()
    return RedirectResponse(url=item.url, status_code=307)


@router.get("/unsubscribe")
def unsubscribe(email: str, db: Session = Depends(get_db)):
    """Remove a user from all future briefings."""
    user = db.query(User).filter(User.email == email).first()
    if user:
        db.delete(user)
        db.commit()
    return HTMLResponse(
        "<html><body style='font-family:system-ui;max-width:480px;margin:4rem auto;padding:0 1rem'>"
        "<h2>Unsubscribed</h2>"
        "<p>You've been removed from Sift. Sorry to see you go.</p>"
        "</body></html>"
    )
