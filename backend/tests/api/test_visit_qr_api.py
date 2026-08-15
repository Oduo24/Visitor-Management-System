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

from tests.factories.user_factory import UserFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.destination_factory import DestinationFactory

from app.services.visit_service import VisitService


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

    return visit


def test_generate_visit_qr(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    response = client.post(
        f"/api/visits/{visit.id}/qr",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["id"] == str(visit.id)
    assert data["qr_token"] is not None
    assert data["qr_generated_at"] is not None

    assert len(data["qr_token"]) > 20


def test_generate_visit_qr_not_found(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    response = client.post(
        f"/api/visits/{uuid.uuid4()}/qr",
        headers=headers,
    )

    assert response.status_code == 404


def test_generate_visit_qr_twice(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    first_response = client.post(
        f"/api/visits/{visit.id}/qr",
        headers=headers,
    )

    assert first_response.status_code == 200

    first_data = (
        first_response
        .get_json()["data"]
    )

    first_token = first_data["qr_token"]

    second_response = client.post(
        f"/api/visits/{visit.id}/qr",
        headers=headers,
    )

    assert second_response.status_code == 409

    second_data = second_response.get_json()

    assert second_data["success"] is False


def test_generate_visit_qr_requires_authentication(
    client,
    session,
):

    visit = seed_visit()

    response = client.post(
        f"/api/visits/{visit.id}/qr"
    )

    assert response.status_code == 401