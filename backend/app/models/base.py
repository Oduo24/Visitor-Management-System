import uuid

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class TimestampMixin:
    """Reusable timestamp columns."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

class AuditMixin:
    """Tracks who created and last updated a record."""

    created_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    updated_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

class UUIDMixin:
    """Reusable UUID primary key."""

    id: Mapped[str] = mapped_column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )