from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError
from app.models.organization import Organization
from app.repositories.organization_repository import OrganizationRepository


class OrganizationService:

    @staticmethod
    def create(data):
        existing = OrganizationRepository.get_by_code(data["code"])

        if existing:
            raise ConflictError("Organization code already exists.")

        organization = Organization(
            name=data["name"],
            code=data["code"],
            email=data.get("email"),
            phone=data.get("phone"),
            website=data.get("website"),
            logo_url=data.get("logo_url"),
            description=data.get("description"),
            is_active=data.get("is_active", True),
        )

        OrganizationRepository.create(organization)

        DatabaseSession.commit()

        return organization

    @staticmethod
    def get_all():
        return OrganizationRepository.get_all()

    @staticmethod
    def get_by_id(organization_id):
        organization = OrganizationRepository.get_by_id(organization_id)

        if not organization:
            raise NotFoundError("Organization not found.")

        return organization

    @staticmethod
    def update(organization_id, data):
        organization = OrganizationRepository.get_by_id(organization_id)

        if not organization:
            raise NotFoundError("Organization not found.")

        # Check if the organization code is changing
        new_code = data.get("code")

        if new_code and new_code != organization.code:
            existing = OrganizationRepository.get_by_code(new_code)

            if existing:
                raise ConflictError("Organization code already exists.")

            organization.code = new_code

        organization.name = data.get("name", organization.name)
        organization.email = data.get("email", organization.email)
        organization.phone = data.get("phone", organization.phone)
        organization.website = data.get("website", organization.website)
        organization.logo_url = data.get("logo_url", organization.logo_url)
        organization.description = data.get(
            "description",
            organization.description,
        )
        organization.is_active = data.get(
            "is_active",
            organization.is_active,
        )

        DatabaseSession.commit()

        return organization

    @staticmethod
    def delete(organization_id):
        organization = OrganizationRepository.get_by_id(organization_id)

        if not organization:
            raise NotFoundError("Organization not found.")

        OrganizationRepository.delete(organization)

        DatabaseSession.commit()