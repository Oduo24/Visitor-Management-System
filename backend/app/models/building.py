from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin


class Building(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "buildings"

    site_id: Mapped[str] = mapped_column(
        ForeignKey("sites.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255)
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    site = relationship(
        "Site",
        back_populates="buildings",
    )

    floors = relationship(
        "Floor",
        back_populates="building",
        cascade="all, delete-orphan",
    )