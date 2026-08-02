from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError
from app.models.site import Site
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository


class SiteService:

    @staticmethod
    def create(data):
        organization = OrganizationRepository.get_by_id(
            data["organization_id"]
        )

        if not organization:
            raise NotFoundError("Organization not found.")

        existing = SiteRepository.get_by_code(data["code"])

        if existing:
            raise ConflictError("Site code already exists.")

        site = Site(
            organization_id=data["organization_id"],
            name=data["name"],
            code=data["code"],
            address=data.get("address"),
            city=data.get("city"),
            country=data.get("country"),
            phone=data.get("phone"),
            email=data.get("email"),
            is_active=data.get("is_active", True),
        )

        SiteRepository.create(site)
        DatabaseSession.commit()

        return site

    @staticmethod
    def get_all():
        return SiteRepository.get_all()

    @staticmethod
    def get_by_id(site_id):
        site = SiteRepository.get_by_id(site_id)

        if not site:
            raise NotFoundError("Site not found.")

        return site

    @staticmethod
    def update(site_id, data):
        site = SiteRepository.get_by_id(site_id)

        if not site:
            raise NotFoundError("Site not found.")

        if (
            "organization_id" in data
            and data["organization_id"] != site.organization_id
        ):
            organization = OrganizationRepository.get_by_id(
                data["organization_id"]
            )

            if not organization:
                raise NotFoundError("Organization not found.")

            site.organization_id = data["organization_id"]

        if (
            "code" in data
            and data["code"] != site.code
        ):
            existing = SiteRepository.get_by_code(data["code"])

            if existing:
                raise ConflictError("Site code already exists.")

            site.code = data["code"]

        site.name = data.get("name", site.name)
        site.address = data.get("address", site.address)
        site.city = data.get("city", site.city)
        site.country = data.get("country", site.country)
        site.phone = data.get("phone", site.phone)
        site.email = data.get("email", site.email)
        site.is_active = data.get("is_active", site.is_active)

        DatabaseSession.commit()

        return site

    @staticmethod
    def delete(site_id):
        site = SiteRepository.get_by_id(site_id)

        if not site:
            raise NotFoundError("Site not found.")

        SiteRepository.delete(site)
        DatabaseSession.commit()