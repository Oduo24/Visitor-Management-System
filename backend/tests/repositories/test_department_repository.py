from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository

from tests.factories.department_factory import DepartmentFactory


def test_create_department(session):
    department = DepartmentFactory()

    OrganizationRepository.create(department.organization)

    DepartmentRepository.create(department)
    DatabaseSession.commit()

    assert department.id is not None


def test_get_by_id(session):
    department = DepartmentFactory()

    OrganizationRepository.create(department.organization)

    DepartmentRepository.create(department)
    DatabaseSession.commit()

    retrieved = DepartmentRepository.get_by_id(department.id)

    assert retrieved is not None
    assert retrieved.id == department.id


def test_get_by_code(session):
    department = DepartmentFactory(code="HR")

    OrganizationRepository.create(department.organization)

    DepartmentRepository.create(department)
    DatabaseSession.commit()

    retrieved = DepartmentRepository.get_by_code("HR")

    assert retrieved is not None
    assert retrieved.code == "HR"


def test_get_all(session):
    department1 = DepartmentFactory(code="HR")
    department2 = DepartmentFactory(
        organization=department1.organization,
        organization_id=department1.organization.id,
        code="FIN",
    )

    OrganizationRepository.create(department1.organization)

    DepartmentRepository.create(department1)
    DepartmentRepository.create(department2)

    DatabaseSession.commit()

    departments = DepartmentRepository.get_all()

    assert len(departments) == 2


def test_delete_department(session):
    department = DepartmentFactory()

    OrganizationRepository.create(department.organization)

    DepartmentRepository.create(department)
    DatabaseSession.commit()

    DepartmentRepository.delete(department)
    DatabaseSession.commit()

    assert DepartmentRepository.get_by_id(department.id) is None