from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.site_factory import SiteFactory
from tests.factories.building_factory import BuildingFactory
from tests.factories.floor_factory import FloorFactory


def test_get_floors(client, session):
    floor = FloorFactory()

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)
    FloorRepository.create(floor)

    DatabaseSession.commit()

    response = client.get("/api/floors")

    assert response.status_code == 200
    assert len(response.get_json()["data"]) == 1


def test_get_floor(client, session):
    floor = FloorFactory()

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)
    FloorRepository.create(floor)

    DatabaseSession.commit()

    response = client.get(f"/api/floors/{floor.id}")

    assert response.status_code == 200


def test_create_floor(client, session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    site = SiteFactory(
        organization=organization,
        organization_id=organization.id,
    )

    SiteRepository.create(site)
    DatabaseSession.commit()

    building = BuildingFactory(
        site=site,
        site_id=site.id,
    )

    BuildingRepository.create(building)
    DatabaseSession.commit()

    payload = {
        "building_id": building.id,
        "name": "Ground Floor",
        "level": 0,
    }

    response = client.post(
        "/api/floors",
        json=payload,
    )

    assert response.status_code == 201


def test_update_floor(client, session):
    floor = FloorFactory()

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)
    FloorRepository.create(floor)

    DatabaseSession.commit()

    response = client.put(
        f"/api/floors/{floor.id}",
        json={
            "name": "Updated Floor"
        },
    )

    assert response.status_code == 200


def test_delete_floor(client, session):
    floor = FloorFactory()

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)
    FloorRepository.create(floor)

    DatabaseSession.commit()

    response = client.delete(
        f"/api/floors/{floor.id}"
    )

    assert response.status_code == 200