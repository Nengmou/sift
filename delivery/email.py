"""Email delivery via Resend — daily digest and magic link emails."""
import logging

import resend
from jinja2 import Environment, FileSystemLoader

from config.settings import get_settings
from db.models import ContentItem, User

logger = logging.getLogger(__name__)
settings = get_settings()

if settings.resend_api_key:
    resend.api_key = settings.resend_api_key

_jinja_env = Environment(
    loader=FileSystemLoader("delivery/templates"),
    autoescape=True,
)


def send_digest(user: User, items: list[ContentItem]) -> str:
    """Render and send the daily digest. Returns Resend message ID (or 'dry-run')."""
    html = _jinja_env.get_template("digest.html").render(
        user=user,
        items=items,
        app_url=settings.app_url,
    )

    if not settings.has_resend:
        logger.info("Dry-run digest for %s (%d items)", user.email, len(items))
        return "dry-run"

    params: resend.Emails.SendParams = {
        "from": settings.email_from,
        "to": [user.email],
        "subject": "Your Sift digest",
        "html": html,
    }
    result = resend.Emails.send(params)
    message_id = result.get("id", "unknown")
    logger.info("Sent digest to %s — message_id=%s", user.email, message_id)
    return message_id


def send_magic_link(email: str, verify_url: str) -> str:
    """Send a magic sign-in link. Returns Resend message ID (or 'dry-run')."""
    if not settings.has_resend:
        logger.info("Dry-run magic link for %s: %s", email, verify_url)
        return "dry-run"

    params: resend.Emails.SendParams = {
        "from": settings.email_from,
        "to": [email],
        "subject": "Your Sift sign-in link",
        "html": (
            "<p style='font-family:system-ui'>Click the link below to sign in to Sift.</p>"
            f"<p><a href='{verify_url}'>Sign in to Sift</a></p>"
            f"<p style='color:#9ca3af;font-size:0.8rem'>"
            f"Link expires in {settings.magic_link_ttl_minutes} minutes.</p>"
        ),
    }
    result = resend.Emails.send(params)
    return result.get("id", "unknown")
