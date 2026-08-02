from app.common.database import DatabaseSession
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository

from tests.factories.building_factory import BuildingFactory


def test_create_building(session):
    building = BuildingFactory()

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)

    BuildingRepository.create(building)
    DatabaseSession.commit()

    assert building.id is not None


def test_get_by_id(session):
    building = BuildingFactory()

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)

    BuildingRepository.create(building)
    DatabaseSession.commit()

    retrieved = BuildingRepository.get_by_id(building.id)

    assert retrieved is not None
    assert retrieved.id == building.id
    assert retrieved.name == building.name


def test_get_by_code(session):
    building = BuildingFactory(code="ADMIN")

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)

    BuildingRepository.create(building)
    DatabaseSession.commit()

    retrieved = BuildingRepository.get_by_code("ADMIN")

    assert retrieved is not None
    assert retrieved.code == "ADMIN"


def test_get_all(session):
    building1 = BuildingFactory()
    building2 = BuildingFactory()

    OrganizationRepository.create(building1.site.organization)
    OrganizationRepository.create(building2.site.organization)

    SiteRepository.create(building1.site)
    SiteRepository.create(building2.site)

    BuildingRepository.create(building1)
    BuildingRepository.create(building2)

    DatabaseSession.commit()

    buildings = BuildingRepository.get_all()

    assert len(buildings) == 2


def test_delete_building(session):
    building = BuildingFactory()

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)

    BuildingRepository.create(building)
    DatabaseSession.commit()

    BuildingRepository.delete(building)
    DatabaseSession.commit()

    assert BuildingRepository.get_by_id(building.id) is None