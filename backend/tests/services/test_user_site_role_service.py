import pytest

from app.common.database import DatabaseSession
from app.common.exceptions import (
    ConflictError,
    NotFoundError,
)

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository

from app.services.user_site_role_service import UserSiteRoleService

from tests.factories.user_factory import UserFactory
from tests.factories.site_factory import SiteFactory
from tests.factories.role_factory import RoleFactory


def test_create_assignment(session):
    user = UserFactory()

    site = SiteFactory(
        organization=user.organization,
        organization_id=user.organization.id,
    )

    role = RoleFactory(
        organization=user.organization,
        organization_id=user.organization.id,
    )

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    SiteRepository.create(site)
    RoleRepository.create(role)
    UserRepository.create(user)

    DatabaseSession.commit()

    created = UserSiteRoleService.create({
        "user_id": user.id,
        "site_id": site.id,
        "role_id": role.id,
    })

    assert created.id is not None


def test_duplicate_assignment(session):
    user = UserFactory()

    site = SiteFactory(
        organization=user.organization,
        organization_id=user.organization.id,
    )

    role = RoleFactory(
        organization=user.organization,
        organization_id=user.organization.id,
    )

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    SiteRepository.create(site)
    RoleRepository.create(role)
    UserRepository.create(user)

    DatabaseSession.commit()

    UserSiteRoleService.create({
        "user_id": user.id,
        "site_id": site.id,
        "role_id": role.id,
    })

    with pytest.raises(ConflictError):
        UserSiteRoleService.create({
            "user_id": user.id,
            "site_id": site.id,
            "role_id": role.id,
        })


def test_delete_assignment(session):
    user = UserFactory()

    site = SiteFactory(
        organization=user.organization,
        organization_id=user.organization.id,
    )

    role = RoleFactory(
        organization=user.organization,
        organization_id=user.organization.id,
    )

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    SiteRepository.create(site)
    RoleRepository.create(role)
    UserRepository.create(user)

    DatabaseSession.commit()

    created = UserSiteRoleService.create({
        "user_id": user.id,
        "site_id": site.id,
        "role_id": role.id,
    })

    UserSiteRoleService.delete(created.id)

    with pytest.raises(NotFoundError):
        UserSiteRoleService.get_by_id(created.id)