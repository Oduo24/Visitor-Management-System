from app.common.database import DatabaseSession
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.site_repository import SiteRepository
from tests.factories.site_factory import SiteFactory


def test_create_site(session):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    assert site.id is not None


def test_get_by_id(session):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    retrieved = SiteRepository.get_by_id(site.id)

    assert retrieved.id == site.id
    assert retrieved.name == site.name


def test_get_by_code(session):
    site = SiteFactory(code="HQ")

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    retrieved = SiteRepository.get_by_code("HQ")

    assert retrieved is not None
    assert retrieved.code == "HQ"


def test_get_all(session):
    site1 = SiteFactory()
    site2 = SiteFactory()

    OrganizationRepository.create(site1.organization)
    OrganizationRepository.create(site2.organization)

    SiteRepository.create(site1)
    SiteRepository.create(site2)

    DatabaseSession.commit()

    sites = SiteRepository.get_all()

    assert len(sites) == 2


def test_delete_site(session):
    site = SiteFactory()

    OrganizationRepository.create(site.organization)
    SiteRepository.create(site)
    DatabaseSession.commit()

    SiteRepository.delete(site)
    DatabaseSession.commit()

    assert SiteRepository.get_by_id(site.id) is None