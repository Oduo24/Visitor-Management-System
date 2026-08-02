from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.department_factory import DepartmentFactory
from tests.factories.user_factory import UserFactory


def test_get_users(client, session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    response = client.get("/api/users")

    assert response.status_code == 200
    assert len(response.get_json()["data"]) == 1


def test_get_user(client, session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    response = client.get(
        f"/api/users/{user.id}"
    )

    assert response.status_code == 200


def test_create_user(client, session):
    organization = OrganizationFactory()

    department = DepartmentFactory(
        organization=organization,
        organization_id=organization.id,
    )

    OrganizationRepository.create(organization)
    DepartmentRepository.create(department)

    DatabaseSession.commit()

    payload = {
        "organization_id": organization.id,
        "department_id": department.id,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@test.com",
        "phone": "0712345678",
        "employee_number": "EMP001",
        "job_title": "ICT Manager",
        "password": "Password123",
    }

    response = client.post(
        "/api/users",
        json=payload,
    )

    assert response.status_code == 201


def test_update_user(client, session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    response = client.put(
        f"/api/users/{user.id}",
        json={
            "job_title": "Finance Manager"
        },
    )

    assert response.status_code == 200


def test_delete_user(client, session):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    response = client.delete(
        f"/api/users/{user.id}"
    )

    assert response.status_code == 200