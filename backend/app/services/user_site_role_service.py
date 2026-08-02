from app.common.database import DatabaseSession
from app.common.exceptions import (
    ConflictError,
    NotFoundError,
)

from app.models.user_site_role import UserSiteRole

from app.repositories.user_repository import UserRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_site_role_repository import (
    UserSiteRoleRepository,
)


class UserSiteRoleService:

    @staticmethod
    def create(data):

        user = UserRepository.get_by_id(
            data["user_id"]
        )

        if not user:
            raise NotFoundError(
                "User not found."
            )

        site = SiteRepository.get_by_id(
            data["site_id"]
        )

        if not site:
            raise NotFoundError(
                "Site not found."
            )

        role = RoleRepository.get_by_id(
            data["role_id"]
        )

        if not role:
            raise NotFoundError(
                "Role not found."
            )

        existing = (
            UserSiteRoleRepository.get_by_user_site_role(
                data["user_id"],
                data["site_id"],
                data["role_id"],
            )
        )

        if existing:
            raise ConflictError(
                "Assignment already exists."
            )

        assignment = UserSiteRole(
            user_id=data["user_id"],
            site_id=data["site_id"],
            role_id=data["role_id"],
        )

        UserSiteRoleRepository.create(
            assignment
        )

        DatabaseSession.commit()

        return assignment

    @staticmethod
    def get_all():
        return UserSiteRoleRepository.get_all()

    @staticmethod
    def get_by_id(record_id):
        assignment = UserSiteRoleRepository.get_by_id(
            record_id
        )

        if not assignment:
            raise NotFoundError(
                "Assignment not found."
            )

        return assignment

    @staticmethod
    def delete(record_id):
        assignment = UserSiteRoleRepository.get_by_id(
            record_id
        )

        if not assignment:
            raise NotFoundError(
                "Assignment not found."
            )

        UserSiteRoleRepository.delete(
            assignment
        )

        DatabaseSession.commit()