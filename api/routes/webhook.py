import logging

from fastapi import APIRouter, Request

router = APIRouter(tags=["webhooks"])
logger = logging.getLogger(__name__)


@router.post("/webhooks/resend")
async def resend_webhook(request: Request):
    """Handle Resend email event webhooks (delivered, bounced, opened, etc.)."""
    payload = await request.json()
    event_type = payload.get("type", "unknown")
    logger.info("Resend webhook: %s", event_type)
    # Post-MVP: parse event, write to interactions table for open tracking
    return {"ok": True, "event": event_type}
