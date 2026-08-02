import pytest

from app.common.exceptions import ConflictError, NotFoundError
from app.common.database import DatabaseSession
from app.repositories.organization_repository import OrganizationRepository
from app.services.organization_service import OrganizationService
from tests.factories.organization_factory import OrganizationFactory

def test_create_organization(session):
    data = {
        "name": "ABC Bank",
        "code": "ABC"
    }

    organization = OrganizationService.create(data)

    assert organization.id is not None
    assert organization.name == "ABC Bank"
    assert organization.code == "ABC"

def test_duplicate_organization_code(session):
    OrganizationRepository.create(
        OrganizationFactory(code="ABC")
    )
    DatabaseSession.commit()

    with pytest.raises(ConflictError):
        OrganizationService.create({
            "name": "Another Org",
            "code": "ABC"
        })

def test_get_all_organizations(session):
    OrganizationRepository.create(OrganizationFactory())
    OrganizationRepository.create(OrganizationFactory())

    DatabaseSession.commit()

    organizations = OrganizationService.get_all()

    assert len(organizations) == 2

def test_get_organization_by_id(session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    retrieved = OrganizationService.get_by_id(organization.id)

    assert retrieved.id == organization.id
    assert retrieved.name == organization.name

def test_get_organization_not_found(session):
    with pytest.raises(NotFoundError):
        OrganizationService.get_by_id("invalid-id")

def test_update_organization(session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    updated = OrganizationService.update(
        organization.id,
        {
            "name": "Updated Name",
            "email": "updated@test.com"
        }
    )

    assert updated.name == "Updated Name"
    assert updated.email == "updated@test.com"

def test_delete_organization(session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    OrganizationService.delete(organization.id)

    with pytest.raises(NotFoundError):
        OrganizationService.get_by_id(organization.id)