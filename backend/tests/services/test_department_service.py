import pytest

from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository

from app.services.department_service import DepartmentService

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.department_factory import DepartmentFactory


def test_create_department(session):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    created = DepartmentService.create({
        "organization_id": organization.id,
        "name": "Human Resources",
        "code": "HR",
        "description": "HR Department",
    })

    assert created.id is not None
    assert created.code == "HR"


def test_duplicate_department_code(session):
    department = DepartmentFactory(code="HR")

    OrganizationRepository.create(department.organization)
    DepartmentRepository.create(department)

    DatabaseSession.commit()

    with pytest.raises(ConflictError):
        DepartmentService.create({
            "organization_id": department.organization.id,
            "name": "Another Department",
            "code": "HR",
        })


def test_invalid_organization(session):
    with pytest.raises(NotFoundError):
        DepartmentService.create({
            "organization_id": "00000000-0000-0000-0000-000000000000",
            "name": "HR",
            "code": "HR",
        })


def test_get_department_by_id(session):
    department = DepartmentFactory()

    OrganizationRepository.create(department.organization)
    DepartmentRepository.create(department)

    DatabaseSession.commit()

    retrieved = DepartmentService.get_by_id(
        department.id
    )

    assert retrieved.id == department.id


def test_update_department(session):
    department = DepartmentFactory()

    OrganizationRepository.create(department.organization)
    DepartmentRepository.create(department)

    DatabaseSession.commit()

    updated = DepartmentService.update(
        department.id,
        {
            "name": "Finance"
        }
    )

    assert updated.name == "Finance"


def test_delete_department(session):
    department = DepartmentFactory()

    OrganizationRepository.create(department.organization)
    DepartmentRepository.create(department)

    DatabaseSession.commit()

    DepartmentService.delete(department.id)

    with pytest.raises(NotFoundError):
        DepartmentService.get_by_id(department.id)