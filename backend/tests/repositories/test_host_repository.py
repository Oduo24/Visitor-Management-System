from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.repositories.host_repository import HostRepository

from tests.factories.user_factory import UserFactory


def test_get_all_hosts(session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    hosts = HostRepository.get_all()

    assert len(hosts) == 1
    assert hosts[0].id == user.id


def test_get_host_by_id(session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    host = HostRepository.get_by_id(user.id)

    assert host is not None
    assert host.id == user.id


def test_search_host(session):
    user = UserFactory(
        first_name="John",
        last_name="Doe",
    )

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    hosts = HostRepository.search("John")

    assert len(hosts) == 1
    assert hosts[0].first_name == "John"


def test_only_active_hosts_returned(session):
    active = UserFactory()
    inactive = UserFactory(
        email="inactive@test.com",
        employee_number="EMP999",
        is_active=False,
    )

    OrganizationRepository.create(active.organization)
    DepartmentRepository.create(active.department)
    UserRepository.create(active)

    OrganizationRepository.create(inactive.organization)
    DepartmentRepository.create(inactive.department)
    UserRepository.create(inactive)

    DatabaseSession.commit()

    hosts = HostRepository.get_all()

    assert len(hosts) == 1
    assert hosts[0].id == active.id