from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import auth, webhook
from config.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Sift",
    version="0.1.0",
    docs_url="/api/docs" if not settings.is_production else None,
    redoc_url=None,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="web/static"), name="static")

from web import routes as web_routes  # noqa: E402
app.include_router(web_routes.router)
app.include_router(auth.router, prefix="/api")
app.include_router(webhook.router, prefix="/api")
