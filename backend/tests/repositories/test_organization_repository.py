from app.models.organization import Organization
from app.repositories.organization_repository import OrganizationRepository
from app.common.database import DatabaseSession
from tests.factories.organization_factory import OrganizationFactory

def test_create_organization(session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    assert organization.id is not None


def test_get_by_id(session):
    organization = OrganizationFactory()
   
    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    retrieved = OrganizationRepository.get_by_id(organization.id)

    assert retrieved is not None
    assert retrieved.id == organization.id
    assert retrieved.name == organization.name


def test_get_by_code(session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    retrieved = OrganizationRepository.get_by_code(organization.code)

    assert retrieved is not None
    assert retrieved.code == organization.code


def test_get_all(session):
    OrganizationRepository.create(OrganizationFactory())
    OrganizationRepository.create(OrganizationFactory())

    DatabaseSession.commit()

    organizations = OrganizationRepository.get_all()

    assert len(organizations) == 2


def test_delete_organization(session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    OrganizationRepository.delete(organization)
    DatabaseSession.commit()

    deleted = OrganizationRepository.get_by_id(organization.id)

    assert deleted is None