from datetime import datetime, timedelta

from app.common.database import DatabaseSession
from app.common.constants import (
    VisitType,
    VisitStatus,
)

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
from tests.factories.destination_factory import (
    DestinationFactory,
)


def seed_visit(
    *,
    visit_type=VisitType.PREBOOKED,
    status=VisitStatus.PENDING,
):

    visitor = VisitorFactory()

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
        "visit_type": visit_type,
        "purpose": "Dashboard Test",
    })

    visit.status = status

    DatabaseSession.commit()

    return visit


def test_visit_dashboard_returns_all_visits(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit_one = seed_visit()
    visit_two = seed_visit()

    response = client.get(
        "/api/visits/dashboard",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 2

    visit_ids = {
        item["id"]
        for item in data
    }

    assert str(visit_one.id) in visit_ids
    assert str(visit_two.id) in visit_ids


def test_visit_dashboard_filters_by_status(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    approved_visit = seed_visit(
        status=VisitStatus.APPROVED
    )

    seed_visit(
        status=VisitStatus.PENDING
    )

    response = client.get(
        "/api/visits/dashboard"
        f"?status={VisitStatus.APPROVED}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == str(
        approved_visit.id
    )
    assert data[0]["status"] == (
        VisitStatus.APPROVED
    )


def test_visit_dashboard_filters_by_site(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    first_visit = seed_visit()
    second_visit = seed_visit()

    response = client.get(
        "/api/visits/dashboard"
        f"?site_id={first_visit.site_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == str(
        first_visit.id
    )


def test_visit_dashboard_filters_by_visit_type(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    prebooked_visit = seed_visit(
        visit_type=VisitType.PREBOOKED
    )

    seed_visit(
        visit_type=VisitType.WALK_IN
    )

    response = client.get(
        "/api/visits/dashboard"
        f"?visit_type={VisitType.PREBOOKED}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == str(
        prebooked_visit.id
    )


def test_visit_dashboard_combines_filters(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    matching_visit = seed_visit(
        visit_type=VisitType.PREBOOKED,
        status=VisitStatus.APPROVED,
    )

    seed_visit(
        visit_type=VisitType.PREBOOKED,
        status=VisitStatus.PENDING,
    )

    seed_visit(
        visit_type=VisitType.WALK_IN,
        status=VisitStatus.APPROVED,
    )

    response = client.get(
        "/api/visits/dashboard"
        f"?status={VisitStatus.APPROVED}"
        f"&site_id={matching_visit.site_id}"
        f"&visit_type={VisitType.PREBOOKED}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == str(
        matching_visit.id
    )


def test_visit_dashboard_filters_by_date_range(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    now = datetime.now()

    start_date = (
        now - timedelta(days=1)
    ).isoformat()

    end_date = (
        now + timedelta(days=1)
    ).isoformat()

    response = client.get(
        "/api/visits/dashboard"
        f"?start_date={start_date}"
        f"&end_date={end_date}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) == 1
    assert data[0]["id"] == str(
        visit.id
    )


def test_visit_dashboard_no_results(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    seed_visit(
        status=VisitStatus.PENDING
    )

    response = client.get(
        "/api/visits/dashboard"
        f"?status={VisitStatus.APPROVED}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data == []


def test_visit_dashboard_requires_authentication(
    client,
    session,
):

    response = client.get(
        "/api/visits/dashboard"
    )

    assert response.status_code == 401