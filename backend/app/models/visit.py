from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin
from app.common.constants import VisitStatus


class Visit(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "visits"

    visitor_id: Mapped[str] = mapped_column(
        ForeignKey("visitors.id"),
        nullable=False,
        index=True,
    )

    host_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    destination_id: Mapped[str] = mapped_column(
        ForeignKey("destinations.id"),
        nullable=False,
        index=True,
    )

    site_id: Mapped[str] = mapped_column(
        ForeignKey("sites.id"),
        nullable=False,
        index=True,
    )

    visit_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=VisitStatus.PENDING,
        index=True,
    )

    purpose: Mapped[str | None] = mapped_column(
        String(500),
    )

    expected_arrival: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    expected_departure: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    checked_in_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    checked_out_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    approved_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id"),
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    badge_number: Mapped[str | None] = mapped_column(
        String(50),
    )

    notes: Mapped[str | None] = mapped_column(
        String(1000),
    )

    qr_token: Mapped[str | None] = mapped_column(
    String(255),
    unique=True,
    index=True,
    )

    qr_generated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    visitor = relationship(
        "Visitor",
        back_populates="visits",
    )

    host = relationship(
        "User",
        foreign_keys=[host_id],
        back_populates="hosted_visits",
    )

    approver = relationship(
        "User",
        foreign_keys=[approved_by],
        back_populates="approved_visits",
    )

    destination = relationship(
        "Destination",
        back_populates="visits",
    )

    site = relationship(
        "Site",
        back_populates="visits",
    )

    audit_logs = relationship(
    "VisitAudit",
    back_populates="visit",
    cascade="all, delete-orphan",
    order_by="VisitAudit.created_at",
    )

    invitations = relationship(
    "VisitInvitation",
    back_populates="visit",
    cascade="all, delete-orphan",
    )

    notifications = relationship(
        "VisitNotification",
        back_populates="visit",
        cascade="all, delete-orphan",
    )