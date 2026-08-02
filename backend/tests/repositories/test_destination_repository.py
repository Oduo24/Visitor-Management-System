from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository
from app.repositories.destination_repository import DestinationRepository

from tests.factories.destination_factory import DestinationFactory


def test_create_destination(session):
    destination = DestinationFactory()

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)

    DestinationRepository.create(destination)
    DatabaseSession.commit()

    assert destination.id is not None


def test_get_by_id(session):
    destination = DestinationFactory()

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)

    DestinationRepository.create(destination)
    DatabaseSession.commit()

    retrieved = DestinationRepository.get_by_id(destination.id)

    assert retrieved is not None
    assert retrieved.id == destination.id


def test_get_by_code(session):
    destination = DestinationFactory(code="HR")

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)

    DestinationRepository.create(destination)
    DatabaseSession.commit()

    retrieved = DestinationRepository.get_by_code("HR")

    assert retrieved is not None
    assert retrieved.code == "HR"


def test_get_all(session):
    destination1 = DestinationFactory(code="HR")
    destination2 = DestinationFactory(
        floor=destination1.floor,
        floor_id=destination1.floor.id,
        code="FIN"
    )

    OrganizationRepository.create(destination1.floor.building.site.organization)
    SiteRepository.create(destination1.floor.building.site)
    BuildingRepository.create(destination1.floor.building)
    FloorRepository.create(destination1.floor)

    DestinationRepository.create(destination1)
    DestinationRepository.create(destination2)

    DatabaseSession.commit()

    destinations = DestinationRepository.get_all()

    assert len(destinations) == 2


def test_delete_destination(session):
    destination = DestinationFactory()

    OrganizationRepository.create(destination.floor.building.site.organization)
    SiteRepository.create(destination.floor.building.site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)

    DestinationRepository.create(destination)
    DatabaseSession.commit()

    DestinationRepository.delete(destination)
    DatabaseSession.commit()

    assert DestinationRepository.get_by_id(destination.id) is None