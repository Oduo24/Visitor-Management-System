
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin


class VisitInvitation(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "visit_invitations"

    visit_id: Mapped[str] = mapped_column(
        ForeignKey("visits.id"),
        nullable=False,
        index=True,
    )

    token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    visit = relationship(
        "Visit",
        back_populates="invitations",
    )