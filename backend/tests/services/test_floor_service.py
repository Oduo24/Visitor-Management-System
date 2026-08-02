import pytest

from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository

from app.services.floor_service import FloorService

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.site_factory import SiteFactory
from tests.factories.building_factory import BuildingFactory
from tests.factories.floor_factory import FloorFactory


def test_create_floor(session):
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

    created = FloorService.create({
        "building_id": building.id,
        "name": "Ground Floor",
        "level": 0,
    })

    assert created.id is not None
    assert created.level == 0


def test_duplicate_floor_level(session):
    floor = FloorFactory(level=1)

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)
    FloorRepository.create(floor)

    DatabaseSession.commit()

    with pytest.raises(ConflictError):
        FloorService.create({
            "building_id": floor.building.id,
            "name": "Another Floor",
            "level": 1,
        })


def test_invalid_building(session):
    with pytest.raises(NotFoundError):
        FloorService.create({
            "building_id": "00000000-0000-0000-0000-000000000000",
            "name": "Ground Floor",
            "level": 0,
        })


def test_get_floor_by_id(session):
    floor = FloorFactory()

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)
    FloorRepository.create(floor)

    DatabaseSession.commit()

    retrieved = FloorService.get_by_id(floor.id)

    assert retrieved.id == floor.id


def test_update_floor(session):
    floor = FloorFactory()

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)
    FloorRepository.create(floor)

    DatabaseSession.commit()

    updated = FloorService.update(
        floor.id,
        {
            "name": "Reception Floor"
        },
    )

    assert updated.name == "Reception Floor"


def test_delete_floor(session):
    floor = FloorFactory()

    OrganizationRepository.create(floor.building.site.organization)
    SiteRepository.create(floor.building.site)
    BuildingRepository.create(floor.building)
    FloorRepository.create(floor)

    DatabaseSession.commit()

    FloorService.delete(floor.id)

    with pytest.raises(NotFoundError):
        FloorService.get_by_id(floor.id)