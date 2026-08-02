from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError

from app.models.department import Department

from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.department_repository import (
    DepartmentRepository,
)


class DepartmentService:

    @staticmethod
    def create(data):
        organization = OrganizationRepository.get_by_id(
            data["organization_id"]
        )

        if not organization:
            raise NotFoundError(
                "Organization not found."
            )

        existing = DepartmentRepository.get_by_code(
            data["code"]
        )

        if existing:
            raise ConflictError(
                "Department code already exists."
            )

        department = Department(
            organization_id=data["organization_id"],
            name=data["name"],
            code=data["code"],
            description=data.get("description"),
            is_active=data.get("is_active", True),
        )

        DepartmentRepository.create(department)
        DatabaseSession.commit()

        return department

    @staticmethod
    def get_all():
        return DepartmentRepository.get_all()

    @staticmethod
    def get_by_id(department_id):
        department = DepartmentRepository.get_by_id(
            department_id
        )

        if not department:
            raise NotFoundError(
                "Department not found."
            )

        return department

    @staticmethod
    def update(department_id, data):
        department = DepartmentRepository.get_by_id(
            department_id
        )

        if not department:
            raise NotFoundError(
                "Department not found."
            )

        if (
            "organization_id" in data
            and data["organization_id"] != department.organization_id
        ):
            organization = OrganizationRepository.get_by_id(
                data["organization_id"]
            )

            if not organization:
                raise NotFoundError(
                    "Organization not found."
                )

            department.organization_id = data["organization_id"]

        if (
            "code" in data
            and data["code"] != department.code
        ):
            existing = DepartmentRepository.get_by_code(
                data["code"]
            )

            if existing:
                raise ConflictError(
                    "Department code already exists."
                )

            department.code = data["code"]

        department.name = data.get(
            "name",
            department.name,
        )

        department.description = data.get(
            "description",
            department.description,
        )

        department.is_active = data.get(
            "is_active",
            department.is_active,
        )

        DatabaseSession.commit()

        return department

    @staticmethod
    def delete(department_id):
        department = DepartmentRepository.get_by_id(
            department_id
        )

        if not department:
            raise NotFoundError(
                "Department not found."
            )

        DepartmentRepository.delete(department)
        DatabaseSession.commit()