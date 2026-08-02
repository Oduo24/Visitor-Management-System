from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.base import UUIDMixin, TimestampMixin


class Site(db.Model, UUIDMixin, TimestampMixin):
    __tablename__ = "sites"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True
    )

    address: Mapped[str | None] = mapped_column(
        String(255)
    )

    city: Mapped[str | None] = mapped_column(
        String(100)
    )

    country: Mapped[str | None] = mapped_column(
        String(100)
    )

    timezone: Mapped[str] = mapped_column(
        String(50),
        default="Africa/Nairobi",
        nullable=False
    )

    phone: Mapped[str | None] = mapped_column(
        String(30)
    )

    email: Mapped[str | None] = mapped_column(
        String(120)
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    organization = relationship(
        "Organization",
        back_populates="sites"
    )

    buildings = relationship(
    "Building",
    back_populates="site",
    cascade="all, delete-orphan"
    )

    user_site_roles = relationship(
    "UserSiteRole",
    back_populates="site",
    cascade="all, delete-orphan",
    )

    visits = relationship(
    "Visit",
    back_populates="site",
    cascade="all, delete-orphan",
    )


    def __repr__(self):
        return f"<Site {self.name}>"