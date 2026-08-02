from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository

from tests.factories.building_factory import BuildingFactory
from tests.factories.organization_factory import OrganizationFactory
from tests.factories.site_factory import SiteFactory


def test_get_buildings(client, session):
    building = BuildingFactory()

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)
    BuildingRepository.create(building)

    DatabaseSession.commit()

    response = client.get("/api/buildings")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert len(data["data"]) == 1


def test_get_building(client, session):
    building = BuildingFactory()

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)
    BuildingRepository.create(building)

    DatabaseSession.commit()

    response = client.get(
        f"/api/buildings/{building.id}"
    )

    assert response.status_code == 200


def test_create_building(client, session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    site = SiteFactory(
        organization=organization,
        organization_id=organization.id,
    )

    SiteRepository.create(site)
    DatabaseSession.commit()

    payload = {
        "site_id": site.id,
        "name": "Administration Block",
        "code": "ADMIN",
    }

    response = client.post(
        "/api/buildings",
        json=payload,
    )

    assert response.status_code == 201


def test_update_building(client, session):
    building = BuildingFactory()

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)
    BuildingRepository.create(building)

    DatabaseSession.commit()

    response = client.put(
        f"/api/buildings/{building.id}",
        json={
            "name": "Updated Building"
        },
    )

    assert response.status_code == 200


def test_delete_building(client, session):
    building = BuildingFactory()

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)
    BuildingRepository.create(building)

    DatabaseSession.commit()

    response = client.delete(
        f"/api/buildings/{building.id}"
    )

    assert response.status_code == 200