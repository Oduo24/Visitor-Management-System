from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.department_factory import DepartmentFactory


def test_get_departments(client, session, auth_headers):
    department = DepartmentFactory()

    OrganizationRepository.create(department.organization)
    DepartmentRepository.create(department)

    DatabaseSession.commit()

    response = client.get(
        "/api/departments",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    department_ids = {
        item["id"]
        for item in data["data"]
    }

    assert str(department.id) in department_ids


def test_get_department(client, session, auth_headers):
    department = DepartmentFactory()

    OrganizationRepository.create(department.organization)
    DepartmentRepository.create(department)

    DatabaseSession.commit()

    response = client.get(
        f"/api/departments/{department.id}",
        headers=auth_headers
    )

    assert response.status_code == 200


def test_create_department(client, session, auth_headers):
    organization = OrganizationFactory()

    OrganizationRepository.create(organization)
    DatabaseSession.commit()

    payload = {
        "organization_id": organization.id,
        "name": "Human Resources",
        "code": "HR",
        "description": "HR Department",
    }

    response = client.post(
        "/api/departments",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 201


def test_update_department(client, session, auth_headers):
    department = DepartmentFactory()

    OrganizationRepository.create(department.organization)
    DepartmentRepository.create(department)

    DatabaseSession.commit()

    response = client.put(
        f"/api/departments/{department.id}",
        json={
            "name": "Finance"
        },
        headers=auth_headers
    )

    assert response.status_code == 200


def test_delete_department(client, session, auth_headers):
    department = DepartmentFactory()

    OrganizationRepository.create(department.organization)
    DepartmentRepository.create(department)

    DatabaseSession.commit()

    response = client.delete(
        f"/api/departments/{department.id}",
        headers=auth_headers
    )

    assert response.status_code == 200