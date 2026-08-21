from datetime import date

from sqlalchemy import (
    String,
    Boolean,
    Date,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin


class Visitor(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "visitors"

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    middle_name: Mapped[str | None] = mapped_column(
        String(100),
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    gender: Mapped[str | None] = mapped_column(
        String(20),
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        index=True,
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=True,
        index=True,
    )

    company: Mapped[str | None] = mapped_column(
        String(255),
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
    )

    nationality: Mapped[str | None] = mapped_column(
        String(100),
    )

    id_number: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    passport_number: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    vehicle_registration: Mapped[str | None] = mapped_column(
        String(50),
        index=True,
    )

    photo_url: Mapped[str | None] = mapped_column(
        String(500),
    )

    is_blacklisted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        String(1000),
    )

    visits = relationship(
    "Visit",
    back_populates="visitor",
    cascade="all, delete-orphan",
    )

    @property
    def full_name(self):
        names = [
            self.first_name,
            self.middle_name,
            self.last_name,
        ]
        return " ".join(filter(None, names))