"""Email delivery via Resend — renders Jinja2 template and sends daily digest."""
import logging

import resend
from jinja2 import Environment, FileSystemLoader

from config.settings import get_settings
from db.models import ContentItem, User

logger = logging.getLogger(__name__)
settings = get_settings()

resend.api_key = settings.resend_api_key

_jinja_env = Environment(
    loader=FileSystemLoader("delivery/templates"),
    autoescape=True,
)


def send_digest(user: User, items: list[ContentItem]) -> str:
    """
    Render and send the daily digest email to `user`.
    Returns the Resend message ID on success.
    """
    html = _jinja_env.get_template("digest.html").render(
        user=user,
        items=items,
        app_url=settings.app_url,
    )

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
