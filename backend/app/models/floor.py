from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin


class Floor(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "floors"

    building_id: Mapped[str] = mapped_column(
        ForeignKey("buildings.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    building = relationship(
        "Building",
        back_populates="floors",
    )

    destinations = relationship(
        "Destination",
        back_populates="floor",
        cascade="all, delete-orphan",
    )