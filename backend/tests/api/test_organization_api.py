from tests.factories.organization_factory import OrganizationFactory

from app.common.database import DatabaseSession
from app.repositories.organization_repository import OrganizationRepository


def test_get_organizations_empty(client):
    response = client.get("/api/organizations")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"] == []


def test_get_organizations(client, session):
    OrganizationRepository.create(OrganizationFactory())
    OrganizationRepository.create(OrganizationFactory())
    DatabaseSession.commit()

    response = client.get("/api/organizations")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert len(data["data"]) == 2


def test_get_organization_by_id(client, session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    response = client.get(
        f"/api/organizations/{organization.id}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["id"] == organization.id
    assert data["data"]["name"] == organization.name


def test_create_organization(client):
    payload = {
        "name": "ABC Bank",
        "code": "ABC",
        "email": "info@abc.com",
        "phone": "0712345678",
        "website": "https://abc.com",
    }

    response = client.post(
        "/api/organizations",
        json=payload,
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True
    assert data["message"] == "Organization created successfully."
    assert data["data"]["name"] == payload["name"]
    assert data["data"]["code"] == payload["code"]


def test_update_organization(client, session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    payload = {
        "name": "Updated Organization",
        "email": "updated@test.com",
    }

    response = client.put(
        f"/api/organizations/{organization.id}",
        json=payload,
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["message"] == "Organization updated successfully."
    assert data["data"]["name"] == "Updated Organization"
    assert data["data"]["email"] == "updated@test.com"


def test_delete_organization(client, session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    response = client.delete(
        f"/api/organizations/{organization.id}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["message"] == "Organization deleted successfully."

    response = client.get(
        f"/api/organizations/{organization.id}"
    )

    assert response.status_code == 404

def test_get_organization_not_found(client):
    response = client.get(
        "/api/organizations/invalid-id"
    )

    assert response.status_code == 404


def test_create_duplicate_organization_code(client):
    payload = {
        "name": "ABC Bank",
        "code": "ABC",
    }

    client.post(
        "/api/organizations",
        json=payload,
    )

    response = client.post(
        "/api/organizations",
        json=payload,
    )

    assert response.status_code == 409