from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository

from tests.factories.user_factory import UserFactory


def test_create_user(session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)

    UserRepository.create(user)
    DatabaseSession.commit()

    assert user.id is not None


def test_get_by_id(session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)

    UserRepository.create(user)
    DatabaseSession.commit()

    retrieved = UserRepository.get_by_id(user.id)

    assert retrieved is not None
    assert retrieved.id == user.id


def test_get_by_email(session):
    user = UserFactory(email="john@test.com")

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)

    UserRepository.create(user)
    DatabaseSession.commit()

    retrieved = UserRepository.get_by_email(
        "john@test.com"
    )

    assert retrieved is not None
    assert retrieved.email == "john@test.com"


def test_get_by_employee_number(session):
    user = UserFactory(employee_number="EMP001")

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)

    UserRepository.create(user)
    DatabaseSession.commit()

    retrieved = UserRepository.get_by_employee_number(
        "EMP001"
    )

    assert retrieved is not None
    assert retrieved.employee_number == "EMP001"


def test_get_all(session):
    user1 = UserFactory()

    user2 = UserFactory(
        organization=user1.organization,
        organization_id=user1.organization.id,
        department=user1.department,
        department_id=user1.department.id,
    )

    OrganizationRepository.create(user1.organization)
    DepartmentRepository.create(user1.department)

    UserRepository.create(user1)
    UserRepository.create(user2)

    DatabaseSession.commit()

    users = UserRepository.get_all()

    assert len(users) == 2


def test_delete_user(session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)

    UserRepository.create(user)
    DatabaseSession.commit()

    UserRepository.delete(user)
    DatabaseSession.commit()

    assert UserRepository.get_by_id(user.id) is None