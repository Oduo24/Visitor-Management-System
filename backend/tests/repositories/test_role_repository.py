from app.common.database import DatabaseSession

from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.role_repository import (
    RoleRepository,
)

from tests.factories.role_factory import RoleFactory


def test_create_role(session):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)

    RoleRepository.create(role)
    DatabaseSession.commit()

    assert role.id is not None


def test_get_by_id(session):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)

    RoleRepository.create(role)
    DatabaseSession.commit()

    retrieved = RoleRepository.get_by_id(role.id)

    assert retrieved is not None
    assert retrieved.id == role.id


def test_get_by_code(session):
    role = RoleFactory(code="ADMIN")

    OrganizationRepository.create(role.organization)

    RoleRepository.create(role)
    DatabaseSession.commit()

    retrieved = RoleRepository.get_by_code("ADMIN")

    assert retrieved is not None
    assert retrieved.code == "ADMIN"


def test_get_all(session):
    role1 = RoleFactory(code="ADMIN")
    role2 = RoleFactory(
        organization=role1.organization,
        organization_id=role1.organization.id,
        code="SECURITY",
    )

    OrganizationRepository.create(role1.organization)

    RoleRepository.create(role1)
    RoleRepository.create(role2)

    DatabaseSession.commit()

    roles = RoleRepository.get_all()

    assert len(roles) == 2


def test_delete_role(session):
    role = RoleFactory()

    OrganizationRepository.create(role.organization)

    RoleRepository.create(role)
    DatabaseSession.commit()

    RoleRepository.delete(role)
    DatabaseSession.commit()

    assert RoleRepository.get_by_id(role.id) is None