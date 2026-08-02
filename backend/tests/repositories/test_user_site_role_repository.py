from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_site_role_repository import UserSiteRoleRepository

from tests.factories.user_site_role_factory import UserSiteRoleFactory


def test_create_assignment(session):
    assignment = UserSiteRoleFactory()

    OrganizationRepository.create(assignment.user.organization)
    DepartmentRepository.create(assignment.user.department)
    SiteRepository.create(assignment.site)
    RoleRepository.create(assignment.role)
    UserRepository.create(assignment.user)

    UserSiteRoleRepository.create(assignment)
    DatabaseSession.commit()

    assert assignment.id is not None


def test_get_by_id(session):
    assignment = UserSiteRoleFactory()

    OrganizationRepository.create(assignment.user.organization)
    DepartmentRepository.create(assignment.user.department)
    SiteRepository.create(assignment.site)
    RoleRepository.create(assignment.role)
    UserRepository.create(assignment.user)

    UserSiteRoleRepository.create(assignment)
    DatabaseSession.commit()

    retrieved = UserSiteRoleRepository.get_by_id(
        assignment.id
    )

    assert retrieved.id == assignment.id


def test_delete_assignment(session):
    assignment = UserSiteRoleFactory()

    OrganizationRepository.create(assignment.user.organization)
    DepartmentRepository.create(assignment.user.department)
    SiteRepository.create(assignment.site)
    RoleRepository.create(assignment.role)
    UserRepository.create(assignment.user)

    UserSiteRoleRepository.create(assignment)
    DatabaseSession.commit()

    UserSiteRoleRepository.delete(assignment)
    DatabaseSession.commit()

    assert UserSiteRoleRepository.get_by_id(
        assignment.id
    ) is None