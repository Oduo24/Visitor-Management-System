import pytest

from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository

from app.services.building_service import BuildingService

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.site_factory import SiteFactory
from tests.factories.building_factory import BuildingFactory


def test_create_building(session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    site = SiteFactory(
        organization=organization,
        organization_id=organization.id,
    )

    SiteRepository.create(site)
    DatabaseSession.commit()

    created = BuildingService.create({
        "site_id": site.id,
        "name": "Administration Block",
        "code": "ADMIN",
        "description": "Main administration building",
    })

    assert created.id is not None
    assert created.code == "ADMIN"


def test_duplicate_building_code(session):
    building = BuildingFactory(code="ADMIN")

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)
    BuildingRepository.create(building)

    DatabaseSession.commit()

    with pytest.raises(ConflictError):
        BuildingService.create({
            "site_id": building.site.id,
            "name": "Another Building",
            "code": "ADMIN",
        })


def test_create_building_invalid_site(session):
    with pytest.raises(NotFoundError):
        BuildingService.create({
            "site_id": "00000000-0000-0000-0000-000000000000",
            "name": "Admin",
            "code": "ADMIN",
        })


def test_get_building_by_id(session):
    building = BuildingFactory()

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)
    BuildingRepository.create(building)

    DatabaseSession.commit()

    retrieved = BuildingService.get_by_id(building.id)

    assert retrieved.id == building.id


def test_update_building(session):
    building = BuildingFactory()

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)
    BuildingRepository.create(building)

    DatabaseSession.commit()

    updated = BuildingService.update(
        building.id,
        {
            "name": "Updated Building"
        }
    )

    assert updated.name == "Updated Building"


def test_delete_building(session):
    building = BuildingFactory()

    OrganizationRepository.create(building.site.organization)
    SiteRepository.create(building.site)
    BuildingRepository.create(building)

    DatabaseSession.commit()

    BuildingService.delete(building.id)

    with pytest.raises(NotFoundError):
        BuildingService.get_by_id(building.id)