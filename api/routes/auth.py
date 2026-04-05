from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from db.session import get_db

router = APIRouter(tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    name: str | None = None


class SignupResponse(BaseModel):
    message: str


@router.post("/signup", response_model=SignupResponse)
def signup(body: SignupRequest, db: Session = Depends(get_db)) -> SignupResponse:
    """
    Create or retrieve a user account and send a magic link email.
    TODO: upsert user, generate magic link token (itsdangerous), send via Resend.
    """
    raise NotImplementedError


@router.get("/auth/verify")
def verify_magic_link(token: str, response: Response, db: Session = Depends(get_db)):
    """
    Validate the magic link token, create a session, set cookie, redirect to /feed.
    TODO: look up token, validate expiry, create UserSession, set secure HttpOnly cookie.
    """
    raise NotImplementedError
