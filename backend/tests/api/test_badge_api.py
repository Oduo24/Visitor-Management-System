import pytest

from app.common.constants import VisitStatus
from app.common.database import DatabaseSession
from app.common.exceptions import NotFoundError

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository
from app.repositories.destination_repository import DestinationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.visitor_repository import VisitorRepository

from app.services.visit_service import VisitService


def seed_visit():

    from tests.factories.visitor_factory import VisitorFactory
    from tests.factories.user_factory import UserFactory
    from tests.factories.destination_factory import DestinationFactory

    visitor = VisitorFactory()
    host = UserFactory()
    destination = DestinationFactory()

    site = destination.floor.building.site

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
        "visit_type": "PREBOOKED",
        "purpose": "Test Visit",
    })

    visit.status = VisitStatus.APPROVED

    DatabaseSession.commit()

    return visit


def test_issue_badge(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    response = client.post(
        f"/api/visits/{visit.id}/badge",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["badge_number"] == "B001"


def test_issue_second_badge(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit_1 = seed_visit()

    response_1 = client.post(
        f"/api/visits/{visit_1.id}/badge",
        headers=headers,
    )

    assert response_1.status_code == 200

    visit_2 = seed_visit()

    response_2 = client.post(
        f"/api/visits/{visit_2.id}/badge",
        headers=headers,
    )

    assert response_2.status_code == 200

    data = response_2.get_json()["data"]

    assert data["badge_number"] == "B002"


def test_issue_badge_twice(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    response_1 = client.post(
        f"/api/visits/{visit.id}/badge",
        headers=headers,
    )

    assert response_1.status_code == 200

    response_2 = client.post(
        f"/api/visits/{visit.id}/badge",
        headers=headers,
    )

    assert response_2.status_code == 409


def test_issue_badge_unapproved_visit(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    visit.status = VisitStatus.PENDING

    DatabaseSession.commit()

    response = client.post(
        f"/api/visits/{visit.id}/badge",
        headers=headers,
    )

    assert response.status_code == 409


def test_issue_badge_visit_not_found(
    client,
    session,
    auth_headers_factory,
):

    import uuid

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    response = client.post(
        f"/api/visits/{uuid.uuid4()}/badge",
        headers=headers,
    )

    assert response.status_code == 404