from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_site_role_repository import UserSiteRoleRepository

from tests.factories.user_factory import UserFactory
from tests.factories.site_factory import SiteFactory
from tests.factories.role_factory import RoleFactory
from tests.factories.user_site_role_factory import UserSiteRoleFactory


def test_get_assignments(client, session, auth_headers):
    assignment = UserSiteRoleFactory()

    OrganizationRepository.create(assignment.user.organization)
    DepartmentRepository.create(assignment.user.department)
    SiteRepository.create(assignment.site)
    RoleRepository.create(assignment.role)
    UserRepository.create(assignment.user)
    UserSiteRoleRepository.create(assignment)

    DatabaseSession.commit()

    response = client.get(
        "/api/user-site-roles",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    assignment_ids = {
        item["id"]
        for item in data["data"]
    }

    assert str(assignment.id) in assignment_ids


def test_create_assignment(client, session, auth_headers):
    user = UserFactory()

    site = SiteFactory(
        organization=user.organization,
        organization_id=user.organization.id,
    )

    role = RoleFactory(
        organization=user.organization,
        organization_id=user.organization.id,
    )

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    SiteRepository.create(site)
    RoleRepository.create(role)
    UserRepository.create(user)

    DatabaseSession.commit()

    payload = {
        "user_id": user.id,
        "site_id": site.id,
        "role_id": role.id,
    }

    response = client.post(
        "/api/user-site-roles",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 201


def test_delete_assignment(client, session, auth_headers):
    user = UserFactory()

    site = SiteFactory(
        organization=user.organization,
        organization_id=user.organization.id,
    )

    role = RoleFactory(
        organization=user.organization,
        organization_id=user.organization.id,
    )

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    SiteRepository.create(site)
    RoleRepository.create(role)
    UserRepository.create(user)

    DatabaseSession.commit()

    created = client.post(
        "/api/user-site-roles",
        json={
            "user_id": user.id,
            "site_id": site.id,
            "role_id": role.id,
        },
    ).get_json()["data"]

    response = client.delete(
        f"/api/user-site-roles/{created['id']}",
        headers=auth_headers
    )

    assert response.status_code == 200