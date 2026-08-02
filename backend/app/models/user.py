from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
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


class User(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    department_id: Mapped[str | None] = mapped_column(
        ForeignKey("departments.id"),
        nullable=True,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
    )

    employee_number: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    job_title: Mapped[str | None] = mapped_column(
        String(150),
    )

    profile_photo_url: Mapped[str | None] = mapped_column(
        String(500),
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    organization = relationship(
        "Organization",
        back_populates="users",
    )

    department = relationship(
        "Department",
        back_populates="users",
    )

    user_site_roles = relationship(
        "UserSiteRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    hosted_visits = relationship(
        "Visit",
        foreign_keys="Visit.host_id",
        back_populates="host",
    )

    approved_visits = relationship(
        "Visit",
        foreign_keys="Visit.approved_by",
        back_populates="approver",
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"