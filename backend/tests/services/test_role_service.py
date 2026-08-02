import pytest

from app.common.database import DatabaseSession
from app.common.exceptions import (
    ConflictError,
    NotFoundError,
)

from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.role_repository import (
    RoleRepository,
)

from app.services.role_service import RoleService

from tests.factories.organization_factory import (
    OrganizationFactory,
)
from tests.factories.role_factory import RoleFactory


def test_create_role(session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    created = RoleService.create({
        "organization_id": organization.id,
        "name": "Administrator",
        "code": "ADMIN",
        "description": "System Administrator",
    })

    assert created.id is not None
    assert created.code == "ADMIN"


def test_duplicate_role_code(session):
    role = RoleFactory(code="ADMIN")

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    with pytest.raises(ConflictError):
        RoleService.create({
            "organization_id": role.organization.id,
            "name": "Another Admin",
            "code": "ADMIN",
        })


def test_invalid_organization(session):
    with pytest.raises(NotFoundError):
        RoleService.create({
            "organization_id": "00000000-0000-0000-0000-000000000000",
            "name": "Administrator",
            "code": "ADMIN",
        })


def test_get_role_by_id(session):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    retrieved = RoleService.get_by_id(role.id)

    assert retrieved.id == role.id


def test_update_role(session):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    updated = RoleService.update(
        role.id,
        {
            "name": "Security Officer",
        },
    )

    assert updated.name == "Security Officer"


def test_delete_role(session):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)
    RoleRepository.create(role)

    DatabaseSession.commit()

    RoleService.delete(role.id)

    with pytest.raises(NotFoundError):
        RoleService.get_by_id(role.id)