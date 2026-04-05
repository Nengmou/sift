from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.deps import get_current_user
from db.models import User

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="web/templates")


@router.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})


@router.get("/feed", response_class=HTMLResponse)
def feed(request: Request, user: User = Depends(get_current_user)):
    # TODO: query ContentItems scored for user.interests, ranked by composite score
    return templates.TemplateResponse(
        "feed.html", {"request": request, "user": user, "items": []}
    )


@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "settings.html", {"request": request, "user": user}
    )


@router.post("/settings", response_class=HTMLResponse)
async def update_settings(request: Request, user: User = Depends(get_current_user)):
    # TODO: parse form, update user.interests and user.delivery_time
    raise NotImplementedError
