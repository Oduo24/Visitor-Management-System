from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError

from app.models.role import Role

from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.role_repository import (
    RoleRepository,
)


class RoleService:

    @staticmethod
    def create(data):
        organization = OrganizationRepository.get_by_id(
            data["organization_id"]
        )

        if not organization:
            raise NotFoundError(
                "Organization not found."
            )

        existing = RoleRepository.get_by_code(
            data["code"]
        )

        if existing:
            raise ConflictError(
                "Role code already exists."
            )

        role = Role(
            organization_id=data["organization_id"],
            name=data["name"],
            code=data["code"],
            description=data.get("description"),
            is_active=data.get("is_active", True),
        )

        RoleRepository.create(role)
        DatabaseSession.commit()

        return role

    @staticmethod
    def get_all():
        return RoleRepository.get_all()

    @staticmethod
    def get_by_id(role_id):
        role = RoleRepository.get_by_id(role_id)

        if not role:
            raise NotFoundError(
                "Role not found."
            )

        return role

    @staticmethod
    def update(role_id, data):
        role = RoleRepository.get_by_id(role_id)

        if not role:
            raise NotFoundError(
                "Role not found."
            )

        if (
            "organization_id" in data
            and data["organization_id"] != role.organization_id
        ):
            organization = OrganizationRepository.get_by_id(
                data["organization_id"]
            )

            if not organization:
                raise NotFoundError(
                    "Organization not found."
                )

            role.organization_id = data["organization_id"]

        if (
            "code" in data
            and data["code"] != role.code
        ):
            existing = RoleRepository.get_by_code(
                data["code"]
            )

            if existing:
                raise ConflictError(
                    "Role code already exists."
                )

            role.code = data["code"]

        role.name = data.get("name", role.name)
        role.description = data.get(
            "description",
            role.description,
        )
        role.is_active = data.get(
            "is_active",
            role.is_active,
        )

        DatabaseSession.commit()

        return role

    @staticmethod
    def delete(role_id):
        role = RoleRepository.get_by_id(role_id)

        if not role:
            raise NotFoundError(
                "Role not found."
            )

        RoleRepository.delete(role)
        DatabaseSession.commit()