from app.common.database import DatabaseSession
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from tests.factories.site_factory import SiteFactory


def test_get_sites(client, session, auth_headers):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)

    DatabaseSession.commit()

    response = client.get(
        "/api/sites",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    site_ids = {
        item["id"]
        for item in data["data"]
    }

    assert str(site.id) in site_ids

def test_get_site(client, session, auth_headers):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    response = client.get(
        f"/api/sites/{site.id}",
        headers=auth_headers
    )

    assert response.status_code == 200


def test_create_site(client, session, auth_headers):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    DatabaseSession.commit()

    payload = {
        "organization_id": site.organization.id,
        "name": "Main Campus",
        "code": "MAIN",
    }

    response = client.post(
        "/api/sites",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 201


def test_update_site(client, session, auth_headers):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    response = client.put(
        f"/api/sites/{site.id}",
        json={
            "name": "Updated Site"
        },
        headers=auth_headers
    )

    assert response.status_code == 200


def test_delete_site(client, session, auth_headers):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    response = client.delete(
        f"/api/sites/{site.id}",
        headers=auth_headers
    )

    assert response.status_code == 200



