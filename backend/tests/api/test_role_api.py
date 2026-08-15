from app.common.database import DatabaseSession

from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.role_repository import (
    RoleRepository,
)

from tests.factories.organization_factory import (
    OrganizationFactory,
)
from tests.factories.role_factory import (
    RoleFactory,
)


def test_get_roles(client, session, auth_headers):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    response = client.get(
        "/api/roles",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    role_ids = {
        item["id"]
        for item in data["data"]
    }

    assert str(role.id) in role_ids


def test_get_role(client, session, auth_headers):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    response = client.get(
        f"/api/roles/{role.id}",
        headers=auth_headers
    )

    assert response.status_code == 200


def test_create_role(client, session, auth_headers):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    payload = {
        "organization_id": organization.id,
        "name": "Administrator",
        "code": "ADMIN",
        "description": "System Administrator",
    }

    response = client.post(
        "/api/roles",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 201


def test_update_role(client, session, auth_headers):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    response = client.put(
        f"/api/roles/{role.id}",
        json={
            "name": "Security Officer",
        },
        headers=auth_headers
    )

    assert response.status_code == 200


def test_delete_role(client, session, auth_headers):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    response = client.delete(
        f"/api/roles/{role.id}",
        headers=auth_headers
    )

    assert response.status_code == 200