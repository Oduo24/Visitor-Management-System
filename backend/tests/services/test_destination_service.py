import pytest

from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository
from app.repositories.destination_repository import DestinationRepository

from app.services.destination_service import DestinationService

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.site_factory import SiteFactory
from tests.factories.building_factory import BuildingFactory
from tests.factories.floor_factory import FloorFactory
from tests.factories.destination_factory import DestinationFactory


def test_create_destination(session):
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

    created = DestinationService.create({
        "floor_id": floor.id,
        "name": "Human Resource Office",
        "code": "HR",
    })

    assert created.id is not None
    assert created.code == "HR"


def test_duplicate_destination_code(session):
    destination = DestinationFactory(code="HR")

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)
    DestinationRepository.create(destination)

    DatabaseSession.commit()

    with pytest.raises(ConflictError):
        DestinationService.create({
            "floor_id": destination.floor.id,
            "name": "Finance",
            "code": "HR",
        })


def test_invalid_floor(session):
    with pytest.raises(NotFoundError):
        DestinationService.create({
            "floor_id": "00000000-0000-0000-0000-000000000000",
            "name": "Finance",
            "code": "FIN",
        })


def test_get_destination_by_id(session):
    destination = DestinationFactory()

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)
    DestinationRepository.create(destination)

    DatabaseSession.commit()

    retrieved = DestinationService.get_by_id(destination.id)

    assert retrieved.id == destination.id


def test_update_destination(session):
    destination = DestinationFactory()

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)
    DestinationRepository.create(destination)

    DatabaseSession.commit()

    updated = DestinationService.update(
        destination.id,
        {
            "name": "Reception"
        },
    )

    assert updated.name == "Reception"


def test_delete_destination(session):
    destination = DestinationFactory()

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)
    DestinationRepository.create(destination)

    DatabaseSession.commit()

    DestinationService.delete(destination.id)

    with pytest.raises(NotFoundError):
        DestinationService.get_by_id(destination.id)