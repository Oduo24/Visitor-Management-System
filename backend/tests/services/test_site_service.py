import pytest

from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from app.services.site_service import SiteService

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.site_factory import SiteFactory

def test_create_site(session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    created = SiteService.create({
        "organization_id": organization.id,
        "name": "Head Office",
        "code": "HQ001",
        "address": "Nairobi",
        "city": "Nairobi",
        "country": "Kenya",
        "phone": "0700000000",
        "email": "hq@test.com",
    })

    assert created.id is not None
    assert created.code == "HQ001"


def test_duplicate_site_code(session):
    site = SiteFactory(code="HQ")

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    with pytest.raises(ConflictError):
        SiteService.create({
            "organization_id": site.organization.id,
            "name": "Another Site",
            "code": "HQ",
        })


def test_create_site_invalid_organization(session):
    with pytest.raises(NotFoundError):
        SiteService.create({
            "organization_id": "00000000-0000-0000-0000-000000000000",
            "name": "HQ",
            "code": "HQ",
        })


def test_get_site_by_id(session):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    retrieved = SiteService.get_by_id(site.id)

    assert retrieved.id == site.id


def test_update_site(session):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    updated = SiteService.update(
        site.id,
        {
            "name": "Updated HQ"
        }
    )

    assert updated.name == "Updated HQ"


def test_delete_site(session):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    SiteService.delete(site.id)

    with pytest.raises(NotFoundError):
        SiteService.get_by_id(site.id)


