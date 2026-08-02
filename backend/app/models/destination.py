from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin


class Destination(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "destinations"

    floor_id: Mapped[str] = mapped_column(
        ForeignKey("floors.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    code: Mapped[str | None] = mapped_column(
        String(30),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    floor = relationship(
        "Floor",
        back_populates="destinations",
    )

    visits = relationship(
        "Visit",
        back_populates="destination",
        cascade="all, delete-orphan",
    )