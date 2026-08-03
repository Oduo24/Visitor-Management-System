import uuid

from app.common.constants import (
    VisitStatus,
    VisitType,
)
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

from tests.factories.visitor_factory import VisitorFactory
from tests.factories.user_factory import UserFactory
from tests.factories.destination_factory import DestinationFactory


def seed_visit():

    visitor = VisitorFactory()
    host = UserFactory()
    destination = DestinationFactory()
    site = destination.floor.building.site

    OrganizationRepository.create(host.organization)
    DepartmentRepository.create(host.department)

    SiteRepository.create(site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)
    DestinationRepository.create(destination)

    UserRepository.create(host)
    VisitorRepository.create(visitor)

    DatabaseSession.flush()

    visit = VisitService.create({
        "visitor_id": visitor.id,
        "host_id": host.id,
        "destination_id": destination.id,
        "site_id": site.id,
        "visit_type": VisitType.PREBOOKED,
        "purpose": "Business Meeting",
    })

    return visit

def test_approve_visit(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory("ORG_ADMIN")

    visit = seed_visit()

    response = client.patch(
        f"/api/visits/{visit.id}/approval",
        json={
            "approved": True,
            "notes": "Approved by security",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["status"] == VisitStatus.APPROVED
    assert data["approved_at"] is not None
    assert data["approved_by"] is not None

def test_reject_visit(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory("ORG_ADMIN")

    visit = seed_visit()

    response = client.patch(
        f"/api/visits/{visit.id}/approval",
        json={
            "approved": False,
            "notes": "Host unavailable",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["status"] == VisitStatus.REJECTED
    assert data["approved_at"] is not None
    assert data["approved_by"] is not None

def test_approve_visit_not_found(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory("ORG_ADMIN")

    response = client.patch(
        f"/api/visits/{uuid.uuid4()}/approval",
        json={
            "approved": True,
        },
        headers=headers,
    )

    assert response.status_code == 404

def test_approve_already_processed_visit(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory("ORG_ADMIN")

    visit = seed_visit()

    client.patch(
        f"/api/visits/{visit.id}/approval",
        json={
            "approved": True,
        },
        headers=headers,
    )

    response = client.patch(
        f"/api/visits/{visit.id}/approval",
        json={
            "approved": False,
        },
        headers=headers,
    )

    assert response.status_code == 409

def test_approve_visit_without_permission(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory("RECEPTIONIST")

    visit = seed_visit()

    response = client.patch(
        f"/api/visits/{visit.id}/approval",
        json={
            "approved": True,
        },
        headers=headers,
    )

    assert response.status_code == 403

