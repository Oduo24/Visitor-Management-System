from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository
from app.repositories.destination_repository import DestinationRepository

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.site_factory import SiteFactory
from tests.factories.building_factory import BuildingFactory
from tests.factories.floor_factory import FloorFactory
from tests.factories.destination_factory import DestinationFactory


def test_get_destinations(client, session, auth_headers):
    destination = DestinationFactory()

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)
    DestinationRepository.create(destination)

    DatabaseSession.commit()

    response = client.get("/api/destinations", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.get_json()["data"]) == 1


def test_get_destination(client, session, auth_headers):
    destination = DestinationFactory()

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)
    DestinationRepository.create(destination)

    DatabaseSession.commit()

    response = client.get(
        f"/api/destinations/{destination.id}",
        headers=auth_headers
    )

    assert response.status_code == 200


def test_create_destination(client, session, auth_headers):
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

    floor = FloorFactory(
        building=building,
        building_id=building.id,
    )
    FloorRepository.create(floor)
    DatabaseSession.commit()

    response = client.post(
        "/api/destinations",
        json={
            "floor_id": floor.id,
            "name": "Human Resource",
            "code": "HR",
        },
        headers=auth_headers
    )

    assert response.status_code == 201


def test_update_destination(client, session, auth_headers):
    destination = DestinationFactory()

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)
    DestinationRepository.create(destination)

    DatabaseSession.commit()

    response = client.put(
        f"/api/destinations/{destination.id}",
        json={
            "name": "Finance"
        },
        headers=auth_headers
    )

    assert response.status_code == 200


def test_delete_destination(client, session, auth_headers):
    destination = DestinationFactory()

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)
    DestinationRepository.create(destination)

    DatabaseSession.commit()

    response = client.delete(
        f"/api/destinations/{destination.id}",
        headers=auth_headers
    )

    assert response.status_code == 200