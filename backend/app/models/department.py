from sqlalchemy import String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin


class Department(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "departments"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"),
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
        Text
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    organization = relationship(
        "Organization",
        back_populates="departments",
    )

    users = relationship(
        "User",
        back_populates="department",
    )