from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository

from tests.factories.floor_factory import FloorFactory


def test_create_floor(session):
    floor = FloorFactory()

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)

    FloorRepository.create(floor)
    DatabaseSession.commit()

    assert floor.id is not None


def test_get_by_id(session):
    floor = FloorFactory()

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)

    FloorRepository.create(floor)
    DatabaseSession.commit()

    retrieved = FloorRepository.get_by_id(floor.id)

    assert retrieved is not None
    assert retrieved.id == floor.id


def test_get_by_building_and_level(session):
    floor = FloorFactory(level=5)

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)

    FloorRepository.create(floor)
    DatabaseSession.commit()

    retrieved = FloorRepository.get_by_building_and_level(
        floor.building.id,
        5,
    )

    assert retrieved is not None
    assert retrieved.level == 5


def test_get_all(session):
    floor1 = FloorFactory(level=1)
    floor2 = FloorFactory(level=2)

    OrganizationRepository.create(floor1.building.site.organization)
    SiteRepository.create(floor1.building.site)
    BuildingRepository.create(floor1.building)

    FloorRepository.create(floor1)
    FloorRepository.create(floor2)

    DatabaseSession.commit()

    floors = FloorRepository.get_all()

    assert len(floors) == 2


def test_delete_floor(session):
    floor = FloorFactory()

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)

    FloorRepository.create(floor)
    DatabaseSession.commit()

    FloorRepository.delete(floor)
    DatabaseSession.commit()

    assert FloorRepository.get_by_id(floor.id) is None