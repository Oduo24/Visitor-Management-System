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


def test_get_roles(client, session):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    response = client.get("/api/roles")

    assert response.status_code == 200
    assert len(response.get_json()["data"]) == 1


def test_get_role(client, session):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    response = client.get(
        f"/api/roles/{role.id}"
    )

    assert response.status_code == 200


def test_create_role(client, session):
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
    )

    assert response.status_code == 201


def test_update_role(client, session):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    response = client.put(
        f"/api/roles/{role.id}",
        json={
            "name": "Security Officer",
        },
    )

    assert response.status_code == 200


def test_delete_role(client, session):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    response = client.delete(
        f"/api/roles/{role.id}"
    )

    assert response.status_code == 200