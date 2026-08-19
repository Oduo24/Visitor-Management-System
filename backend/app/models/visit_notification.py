
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin


class VisitNotification(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "visit_notifications"

    visit_id: Mapped[str] = mapped_column(
        ForeignKey("visits.id"),
        nullable=False,
        index=True,
    )

    recipient: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    channel: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    event: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    subject: Mapped[str | None] = mapped_column(
        String(255),
    )

    message: Mapped[str | None] = mapped_column(
        Text,
    )

    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
    )

    visit = relationship(
        "Visit",
        back_populates="notifications",
    )