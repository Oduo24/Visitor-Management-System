import pytest

from app.common.database import DatabaseSession
from app.common.exceptions import NotFoundError

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository

from app.services.host_service import HostService

from tests.factories.user_factory import UserFactory


def test_get_all_hosts(session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    hosts = HostService.get_all()

    assert len(hosts) == 1


def test_get_host(session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    host = HostService.get_by_id(user.id)

    assert host.id == user.id


def test_host_not_found(session):

    with pytest.raises(NotFoundError):
        HostService.get_by_id(
            "11111111-1111-1111-1111-111111111111"
        )


def test_search_hosts(session):
    user = UserFactory(
        first_name="Alice",
    )

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    hosts = HostService.search("Alice")

    assert len(hosts) == 1
    assert hosts[0].first_name == "Alice"