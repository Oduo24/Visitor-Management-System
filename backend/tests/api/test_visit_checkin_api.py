import uuid

from app.common.constants import VisitStatus
from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository
from app.repositories.destination_repository import DestinationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.visitor_repository import VisitorRepository

from app.services.visit_service import VisitService
from app.services.badge_service import BadgeService

from tests.factories.visitor_factory import VisitorFactory
from tests.factories.user_factory import UserFactory
from tests.factories.destination_factory import DestinationFactory


def seed_approved_visit():

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

    BadgeService.issue(
        visit.id
    )

    return visit


def test_check_in_visit(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_approved_visit()

    response = client.post(
        f"/api/visits/{visit.id}/check-in",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["status"] == VisitStatus.CHECKED_IN
    assert data["checked_in_at"] is not None
    assert data["badge_number"] is not None


def test_check_in_without_badge(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

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

    response = client.post(
        f"/api/visits/{visit.id}/check-in",
        headers=headers,
    )

    assert response.status_code == 409


def test_check_in_pending_visit(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_approved_visit()

    visit.status = VisitStatus.PENDING

    DatabaseSession.commit()

    response = client.post(
        f"/api/visits/{visit.id}/check-in",
        headers=headers,
    )

    assert response.status_code == 409


def test_check_in_already_checked_in_visit(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_approved_visit()

    response = client.post(
        f"/api/visits/{visit.id}/check-in",
        headers=headers,
    )

    assert response.status_code == 200

    response = client.post(
        f"/api/visits/{visit.id}/check-in",
        headers=headers,
    )

    assert response.status_code == 409


def test_check_in_visit_not_found(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    response = client.post(
        f"/api/visits/{uuid.uuid4()}/check-in",
        headers=headers,
    )

    assert response.status_code == 404