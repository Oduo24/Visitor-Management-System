from app.common.database import DatabaseSession

from app.repositories.visitor_repository import VisitorRepository

from tests.factories.visitor_factory import VisitorFactory


def test_get_visitors(client, session, auth_headers):

    visitor = VisitorFactory()

    VisitorRepository.create(visitor)

    DatabaseSession.commit()

    response = client.get(
        "/api/visitors",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_get_visitor(client, session, auth_headers):

    visitor = VisitorFactory()

    VisitorRepository.create(visitor)

    DatabaseSession.commit()

    response = client.get(
        f"/api/visitors/{visitor.id}",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_search_visitors(client, session, auth_headers):

    visitor = VisitorFactory(
        first_name="John"
    )

    VisitorRepository.create(visitor)

    DatabaseSession.commit()

    response = client.get(
        "/api/visitors?q=John",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["first_name"] == "John"


def test_create_visitor(client,session, auth_headers):

    payload = {

        "first_name": "John",
        "last_name": "Doe",
        "phone": "0712345678",
        "id_number": "12345678",

    }

    response = client.post(
        "/api/visitors",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 201


def test_delete_visitor(client, session, auth_headers):

    visitor = VisitorFactory()

    VisitorRepository.create(visitor)

    DatabaseSession.commit()

    response = client.delete(
        f"/api/visitors/{visitor.id}",
        headers=auth_headers,
    )

    assert response.status_code == 200