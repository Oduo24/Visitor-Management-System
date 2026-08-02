from app.authorization.role_permissions import ROLE_PERMISSIONS


class AuthorizationService:

    @staticmethod
    def has_permission(user, permission):

        if not user:
            return False

        for assignment in user.user_site_roles:

            permissions = ROLE_PERMISSIONS.get(
                assignment.role.code,
                set(),
            )

            if "*" in permissions:
                return True

            if permission in permissions:
                return True

        return False

    @staticmethod
    def has_site_permission(
        user,
        site_id,
        permission,
    ):

        if not user:
            return False

        for assignment in user.user_site_roles:

            if assignment.site_id != site_id:
                continue

            permissions = ROLE_PERMISSIONS.get(
                assignment.role.code,
                set(),
            )

            if "*" in permissions:
                return True

            if permission in permissions:
                return True

        return False

    @staticmethod
    def get_site_ids(user):

        return [
            assignment.site_id
            for assignment in user.user_site_roles
        ]

    @staticmethod
    def has_site_access(
        user,
        site_id,
    ):

        return site_id in AuthorizationService.get_site_ids(
            user
        )