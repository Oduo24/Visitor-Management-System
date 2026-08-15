import uuid
from datetime import datetime, timezone
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

from tests.factories.user_factory import UserFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.destination_factory import DestinationFactory


def seed_visit():

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

    visit.status = VisitStatus.CHECKED_IN
    visit.badge_number = "BADGE-0001"
    visit.checked_in_at = datetime.now(
        timezone.utc
    )

    DatabaseSession.commit()

    return visit


def test_check_out_visit(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    response = client.post(
        f"/api/visits/{visit.id}/check-out",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["id"] == str(visit.id)
    assert data["status"] == VisitStatus.CHECKED_OUT
    assert data["checked_out_at"] is not None


def test_check_out_visit_not_found(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    response = client.post(
        f"/api/visits/{uuid.uuid4()}/check-out",
        headers=headers,
    )

    assert response.status_code == 404


def test_check_out_visit_not_checked_in(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    visit.status = VisitStatus.APPROVED
    visit.checked_in_at = None

    DatabaseSession.commit()

    response = client.post(
        f"/api/visits/{visit.id}/check-out",
        headers=headers,
    )

    assert response.status_code == 409

    data = response.get_json()

    assert data["success"] is False


def test_check_out_visit_already_checked_out(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    first_response = client.post(
        f"/api/visits/{visit.id}/check-out",
        headers=headers,
    )

    assert first_response.status_code == 200

    second_response = client.post(
        f"/api/visits/{visit.id}/check-out",
        headers=headers,
    )

    assert second_response.status_code == 409

    data = second_response.get_json()

    assert data["success"] is False


def test_check_out_visit_requires_authentication(
    client,
    session,
):

    visit = seed_visit()

    response = client.post(
        f"/api/visits/{visit.id}/check-out"
    )

    assert response.status_code == 401