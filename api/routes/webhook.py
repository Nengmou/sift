from fastapi import APIRouter, Request

router = APIRouter(tags=["webhooks"])


@router.post("/webhooks/resend")
async def resend_webhook(request: Request):
    """
    Handle Resend email event webhooks (delivered, bounced, opened, etc.).
    TODO: verify Resend signature header, parse event, log to interactions table.
    """
    raise NotImplementedError
