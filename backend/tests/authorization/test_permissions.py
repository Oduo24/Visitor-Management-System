from app.authorization.permissions import Permission
from app.services.authorization_service import AuthorizationService

from tests.factories.user_site_role_factory import UserSiteRoleFactory


def test_super_admin_has_all_permissions():

    assignment = UserSiteRoleFactory()
    assignment.role.code = "SUPER_ADMIN"

    assignment.user.user_site_roles = [assignment]

    assert AuthorizationService.has_permission(
        assignment.user,
        Permission.USER_DELETE,
    )


def test_receptionist_cannot_delete_users():

    assignment = UserSiteRoleFactory()
    assignment.role.code = "RECEPTIONIST"

    assignment.user.user_site_roles = [assignment]

    assert not AuthorizationService.has_permission(
        assignment.user,
        Permission.USER_DELETE,
    )


def test_receptionist_can_create_visitors():

    assignment = UserSiteRoleFactory()
    assignment.role.code = "RECEPTIONIST"

    assignment.user.user_site_roles = [assignment]

    assert AuthorizationService.has_permission(
        assignment.user,
        Permission.VISITOR_CREATE,
    )