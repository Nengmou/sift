from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from api.routes import auth, webhook
from config.settings import get_settings
from db.session import SessionLocal

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


@app.get("/livez")
def livecheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return {"status": "ok"}
