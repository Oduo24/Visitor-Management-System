from werkzeug.security import generate_password_hash

from app.common.database import DatabaseSession
from app.common.exceptions import (
    ConflictError,
    NotFoundError,
)

from app.models.user import User

from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.department_repository import (
    DepartmentRepository,
)
from app.repositories.user_repository import (
    UserRepository,
)


class UserService:

    @staticmethod
    def create(data):

        organization = OrganizationRepository.get_by_id(
            data["organization_id"]
        )

        if not organization:
            raise NotFoundError(
                "Organization not found."
            )

        if data.get("department_id"):
            department = DepartmentRepository.get_by_id(
                data["department_id"]
            )

            if not department:
                raise NotFoundError(
                    "Department not found."
                )

        if UserRepository.get_by_email(data["email"]):
            raise ConflictError(
                "Email already exists."
            )

        employee_number = data.get("employee_number")

        if (
            employee_number
            and UserRepository.get_by_employee_number(
                employee_number
            )
        ):
            raise ConflictError(
                "Employee number already exists."
            )

        user = User(
            organization_id=data["organization_id"],
            department_id=data.get("department_id"),
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data.get("phone"),
            employee_number=employee_number,
            job_title=data.get("job_title"),
            profile_photo_url=data.get(
                "profile_photo_url"
            ),
            password_hash=generate_password_hash(
                data["password"]
            ),
            is_active=data.get(
                "is_active",
                True,
            ),
        )

        UserRepository.create(user)
        DatabaseSession.commit()

        return user

    @staticmethod
    def get_all():
        return UserRepository.get_all()

    @staticmethod
    def get_by_id(user_id):
        user = UserRepository.get_by_id(user_id)

        if not user:
            raise NotFoundError(
                "User not found."
            )

        return user

    @staticmethod
    def update(user_id, data):
        user = UserRepository.get_by_id(user_id)

        if not user:
            raise NotFoundError(
                "User not found."
            )

        if (
            "organization_id" in data
            and data["organization_id"] != user.organization_id
        ):
            organization = OrganizationRepository.get_by_id(
                data["organization_id"]
            )

            if not organization:
                raise NotFoundError(
                    "Organization not found."
                )

            user.organization_id = data["organization_id"]

        if "department_id" in data:
            if data["department_id"] is not None:
                department = DepartmentRepository.get_by_id(
                    data["department_id"]
                )

                if not department:
                    raise NotFoundError(
                        "Department not found."
                    )

            user.department_id = data["department_id"]

        if (
            "email" in data
            and data["email"] != user.email
        ):
            existing = UserRepository.get_by_email(
                data["email"]
            )

            if existing:
                raise ConflictError(
                    "Email already exists."
                )

            user.email = data["email"]

        if (
            "employee_number" in data
            and data["employee_number"] != user.employee_number
        ):
            if data["employee_number"]:
                existing = UserRepository.get_by_employee_number(
                    data["employee_number"]
                )

                if existing:
                    raise ConflictError(
                        "Employee number already exists."
                    )

            user.employee_number = data["employee_number"]

        user.first_name = data.get(
            "first_name",
            user.first_name,
        )

        user.last_name = data.get(
            "last_name",
            user.last_name,
        )

        user.phone = data.get(
            "phone",
            user.phone,
        )

        user.job_title = data.get(
            "job_title",
            user.job_title,
        )

        user.profile_photo_url = data.get(
            "profile_photo_url",
            user.profile_photo_url,
        )

        if "password" in data:
            user.password_hash = generate_password_hash(
                data["password"]
            )

        user.is_active = data.get(
            "is_active",
            user.is_active,
        )

        DatabaseSession.commit()

        return user

    @staticmethod
    def delete(user_id):
        user = UserRepository.get_by_id(user_id)

        if not user:
            raise NotFoundError(
                "User not found."
            )

        UserRepository.delete(user)
        DatabaseSession.commit()