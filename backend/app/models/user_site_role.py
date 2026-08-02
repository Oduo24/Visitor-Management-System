from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin


class UserSiteRole(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "user_site_roles"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "site_id",
            "role_id",
            name="uq_user_site_role",
        ),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    site_id: Mapped[str] = mapped_column(
        ForeignKey("sites.id"),
        nullable=False,
        index=True,
    )

    role_id: Mapped[str] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="user_site_roles",
    )

    site = relationship(
        "Site",
        back_populates="user_site_roles",
    )

    role = relationship(
        "Role",
        back_populates="user_site_roles",
    )