from sqlalchemy import (
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin


class VisitAudit(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "visit_audits"

    visit_id: Mapped[str] = mapped_column(
        ForeignKey("visits.id"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(1000),
    )

    visit = relationship(
        "Visit",
        back_populates="audit_logs",
    )

    user = relationship(
        "User",
    )