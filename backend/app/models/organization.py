from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import UUIDMixin, TimestampMixin
from app.extensions import db


class Organization(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True
    )

    email: Mapped[str | None] = mapped_column(
        String(120)
    )

    phone: Mapped[str | None] = mapped_column(
        String(30)
    )

    website: Mapped[str | None] = mapped_column(
        String(255)
    )

    logo_url: Mapped[str | None] = mapped_column(
        String(255)
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(255)
    )

    sites = relationship(
    "Site",
    back_populates="organization",
    cascade="all, delete-orphan"
    )

    departments = relationship(
    "Department",
    back_populates="organization",
    cascade="all, delete-orphan",
    )

    roles = relationship(
    "Role",
    back_populates="organization",
    cascade="all, delete-orphan",
    )

    users = relationship(
    "User",
    back_populates="organization",
    cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Organization {self.name}>"