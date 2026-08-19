import pytest

from app.common.database import DatabaseSession
from app.common.constants import VisitType

from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.department_repository import (
    DepartmentRepository,
)
from app.repositories.site_repository import (
    SiteRepository,
)
from app.repositories.building_repository import (
    BuildingRepository,
)
from app.repositories.floor_repository import (
    FloorRepository,
)
from app.repositories.destination_repository import (
    DestinationRepository,
)
from app.repositories.user_repository import (
    UserRepository,
)
from app.repositories.visitor_repository import (
    VisitorRepository,
)

from app.services.visit_service import VisitService

from tests.factories.user_factory import UserFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.destination_factory import DestinationFactory


def seed_visit(
    first_name="John",
    last_name="Doe",
    phone="0712345678",
    id_number="ID100001",
    passport_number="P100001",
):

    visitor = VisitorFactory(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        id_number=id_number,
        passport_number=passport_number,
    )

    host = UserFactory()

    destination = DestinationFactory()

    site = (
        destination
        .floor
        .building
        .site
    )

    OrganizationRepository.create(
        host.organization
    )

    DepartmentRepository.create(
        host.department
    )

    SiteRepository.create(
        site
    )

    BuildingRepository.create(
        destination.floor.building
    )

    FloorRepository.create(
        destination.floor
    )

    DestinationRepository.create(
        destination
    )

    UserRepository.create(
        host
    )

    VisitorRepository.create(
        visitor
    )

    DatabaseSession.flush()

    visit = VisitService.create({
        "visitor_id": visitor.id,
        "host_id": host.id,
        "destination_id": destination.id,
        "site_id": site.id,
        "visit_type": VisitType.PREBOOKED,
        "purpose": "Search Test",
    })

    return visit


def test_search_visit_by_first_name(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit(
        first_name="Gerald",
        last_name="Ochieng",
        phone="0711111111",
        id_number="ID200001",
        passport_number="P200001",
    )

    response = client.get(
        "/api/visits/search?q=Gerald",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == str(visit.id)
    assert data[0]["visitor_id"] == str(
        visit.visitor_id
    )


def test_search_visit_by_last_name(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit(
        first_name="Jane",
        last_name="Kamau",
        phone="0722222222",
        id_number="ID200002",
        passport_number="P200002",
    )

    response = client.get(
        "/api/visits/search?q=Kamau",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == str(visit.id)


def test_search_visit_by_phone(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit(
        first_name="Peter",
        last_name="Otieno",
        phone="0733333333",
        id_number="ID200003",
        passport_number="P200003",
    )

    response = client.get(
        "/api/visits/search?q=0733333333",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == str(visit.id)


def test_search_visit_by_id_number(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit(
        first_name="Alice",
        last_name="Akinyi",
        phone="0744444444",
        id_number="ID200004",
        passport_number="P200004",
    )

    response = client.get(
        "/api/visits/search?q=ID200004",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == str(visit.id)


def test_search_visit_no_results(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    seed_visit(
        first_name="David",
        last_name="Onyango",
        phone="0755555555",
        id_number="ID200005",
        passport_number="P200005",
    )

    response = client.get(
        "/api/visits/search?q=DoesNotExist",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data == []


def test_search_visits_without_query(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit(
        first_name="Michael",
        last_name="Ouma",
        phone="0766666666",
        id_number="ID200006",
        passport_number="P200006",
    )

    response = client.get(
        "/api/visits/search",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == str(visit.id)


def test_search_visits_requires_authentication(
    client,
    session,
):

    response = client.get(
        "/api/visits/search?q=John"
    )

    assert response.status_code == 401