import pytest

from werkzeug.security import check_password_hash

from app.common.database import DatabaseSession
from app.common.exceptions import (
    ConflictError,
    NotFoundError,
)

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository

from app.services.user_service import UserService

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.department_factory import DepartmentFactory
from tests.factories.user_factory import UserFactory


def test_create_user(session):
    organization = OrganizationFactory()

    department = DepartmentFactory(
        organization=organization,
        organization_id=organization.id,
    )

    OrganizationRepository.create(organization)
    DepartmentRepository.create(department)

    DatabaseSession.commit()

    created = UserService.create({
        "organization_id": organization.id,
        "department_id": department.id,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@test.com",
        "phone": "0712345678",
        "employee_number": "EMP001",
        "job_title": "Manager",
        "password": "Password123",
    })

    assert created.id is not None
    assert check_password_hash(
        created.password_hash,
        "Password123"
    )


def test_duplicate_email(session):
    user = UserFactory(email="john@test.com")

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    with pytest.raises(ConflictError):
        UserService.create({
            "organization_id": user.organization.id,
            "department_id": user.department.id,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "john@test.com",
            "password": "Password123",
        })


def test_invalid_organization(session):
    with pytest.raises(NotFoundError):
        UserService.create({
            "organization_id": "00000000-0000-0000-0000-000000000000",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@test.com",
            "password": "Password123",
        })


def test_get_user(session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    retrieved = UserService.get_by_id(user.id)

    assert retrieved.id == user.id


def test_update_user(session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    updated = UserService.update(
        user.id,
        {
            "job_title": "ICT Manager"
        },
    )

    assert updated.job_title == "ICT Manager"


def test_delete_user(session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    UserService.delete(user.id)

    with pytest.raises(NotFoundError):
        UserService.get_by_id(user.id)