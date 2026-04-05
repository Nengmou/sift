import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

SourceEnum = Enum(
    "hn", "rss", "reddit", "twitter", "youtube",
    name="source_enum",
)

ContentTypeEnum = Enum(
    "article", "thread", "video", "post", "comment",
    name="content_type_enum",
)

ActionEnum = Enum(
    "click", "open", "dismiss",
    name="action_enum",
)

SourceSurfaceEnum = Enum(
    "email", "web",
    name="source_surface_enum",
)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_magic_link_token", "magic_link_token"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    interests: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    delivery_time: Mapped[str | None] = mapped_column(
        String(5), nullable=True, comment="HH:MM in UTC, e.g. '08:00'"
    )
    magic_link_token: Mapped[str | None] = mapped_column(String(512), nullable=True)
    magic_link_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utcnow
    )

    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession", back_populates="user", cascade="all, delete-orphan"
    )
    interactions: Mapped[list["Interaction"]] = relationship(
        "Interaction", back_populates="user", cascade="all, delete-orphan"
    )


# ---------------------------------------------------------------------------
# Content Items
# ---------------------------------------------------------------------------

class ContentItem(Base):
    __tablename__ = "content_items"
    __table_args__ = (
        UniqueConstraint("source", "source_id", name="uq_content_source_source_id"),
        Index("ix_content_items_source", "source"),
        Index("ix_content_items_published_at", "published_at"),
        Index("ix_content_items_quality_score", "quality_score"),
        Index("ix_content_items_ingested_at", "ingested_at"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    source: Mapped[str] = mapped_column(SourceEnum, nullable=False)
    source_id: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    authenticity_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    anxiety_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    content_type: Mapped[str | None] = mapped_column(ContentTypeEnum, nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, nullable=False, default=dict)
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utcnow
    )

    interactions: Mapped[list["Interaction"]] = relationship(
        "Interaction", back_populates="content_item", cascade="all, delete-orphan"
    )


# ---------------------------------------------------------------------------
# Interactions
# ---------------------------------------------------------------------------

class Interaction(Base):
    __tablename__ = "interactions"
    __table_args__ = (
        Index("ix_interactions_user_id", "user_id"),
        Index("ix_interactions_content_id", "content_id"),
        Index("ix_interactions_timestamp", "timestamp"),
        Index("ix_interactions_user_content", "user_id", "content_id"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    content_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("content_items.id", ondelete="CASCADE"),
        nullable=False,
    )
    action: Mapped[str] = mapped_column(ActionEnum, nullable=False)
    source_surface: Mapped[str] = mapped_column(SourceSurfaceEnum, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utcnow
    )

    user: Mapped["User"] = relationship("User", back_populates="interactions")
    content_item: Mapped["ContentItem"] = relationship(
        "ContentItem", back_populates="interactions"
    )


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------

class UserSession(Base):
    __tablename__ = "sessions"
    __table_args__ = (
        Index("ix_sessions_token", "token", unique=True),
        Index("ix_sessions_user_id", "user_id"),
        Index("ix_sessions_expires_at", "expires_at"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    token: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utcnow
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="sessions")
