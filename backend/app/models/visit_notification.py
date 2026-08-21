from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.extensions import db
from app.models.base import (
    UUIDMixin,
    TimestampMixin,
)


class VisitNotification(
    db.Model,
    UUIDMixin,
    TimestampMixin,
):

    __tablename__ = "visit_notifications"

    visit_id: Mapped[str] = mapped_column(
        ForeignKey("visits.id"),
        nullable=False,
        index=True,
    )

    recipient: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    channel: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    event: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    subject: Mapped[str | None] = mapped_column(
        String(255),
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    provider_message_id: Mapped[str | None] = mapped_column(
        String(255),
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