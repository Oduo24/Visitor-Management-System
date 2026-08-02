from app.authorization.permissions import Permission
from app.services.authorization_service import AuthorizationService

from tests.factories.user_site_role_factory import (
    UserSiteRoleFactory,
)


def test_has_site_permission():

    assignment = UserSiteRoleFactory()

    assignment.role.code = "RECEPTIONIST"

    assignment.user.user_site_roles = [
        assignment
    ]

    assert AuthorizationService.has_site_permission(
        assignment.user,
        assignment.site.id,
        Permission.VISITOR_CREATE,
    )


def test_wrong_site_returns_false():

    assignment = UserSiteRoleFactory()

    assignment.role.code = "RECEPTIONIST"

    assignment.user.user_site_roles = [
        assignment
    ]

    assert not AuthorizationService.has_site_permission(
        assignment.user,
        "another-site-id",
        Permission.VISITOR_CREATE,
    )


def test_get_site_ids():

    assignment = UserSiteRoleFactory()

    assignment.user.user_site_roles = [
        assignment
    ]

    assert assignment.site.id in (
        AuthorizationService.get_site_ids(
            assignment.user
        )
    )