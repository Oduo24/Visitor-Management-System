from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository

from tests.factories.user_factory import UserFactory


def test_get_hosts(client, session, auth_headers):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    response = client.get("/api/hosts", headers=auth_headers)

    assert response.status_code == 200


def test_get_host(client, session, auth_headers):
    user = UserFactory()

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    response = client.get(
        f"/api/hosts/{user.id}",
        headers=auth_headers,
    )
    

    assert response.status_code == 200


def test_search_hosts(client, session, auth_headers):
    user = UserFactory(
        first_name="Jane",
    )

    OrganizationRepository.create(user.organization)
    DepartmentRepository.create(user.department)
    UserRepository.create(user)

    DatabaseSession.commit()

    response = client.get(
        "/api/hosts?q=Jane",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["first_name"] == "Jane"


def test_get_host_not_found(client, auth_headers):

    response = client.get(
        "/api/hosts/11111111-1111-1111-1111-111111111111",
        headers=auth_headers,
    )

    assert response.status_code == 404