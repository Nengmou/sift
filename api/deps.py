from datetime import UTC, datetime

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.models import User, UserSession
from db.session import get_db


def get_current_user(
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    """Dependency that enforces authentication via session cookie."""
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    session = (
        db.query(UserSession)
        .filter(
            UserSession.token == session_token,
            UserSession.expires_at > datetime.now(UTC),
        )
        .first()
    )
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return session.user
