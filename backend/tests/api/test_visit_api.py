from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository
from app.repositories.destination_repository import DestinationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.visitor_repository import VisitorRepository

from tests.factories.visit_factory import VisitFactory


def test_get_visits(client, session, auth_headers):

    visit = VisitFactory()

    OrganizationRepository.create(visit.host.organization)
    DepartmentRepository.create(visit.host.department)

    SiteRepository.create(visit.site)
    BuildingRepository.create(visit.destination.floor.building)
    FloorRepository.create(visit.destination.floor)
    DestinationRepository.create(visit.destination)

    UserRepository.create(visit.host)
    VisitorRepository.create(visit.visitor)

    DatabaseSession.commit()

    client.post(
        "/api/visits",
        json={
            "visitor_id": visit.visitor.id,
            "host_id": visit.host.id,
            "destination_id": visit.destination.id,
            "site_id": visit.site.id,
            "visit_type": visit.visit_type,
            "purpose": visit.purpose,
        },
        headers=auth_headers,
    )

    response = client.get(
        "/api/visits",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_get_visit(client, session, auth_headers):

    visit = VisitFactory()

    OrganizationRepository.create(visit.host.organization)
    DepartmentRepository.create(visit.host.department)

    SiteRepository.create(visit.site)
    BuildingRepository.create(visit.destination.floor.building)
    FloorRepository.create(visit.destination.floor)
    DestinationRepository.create(visit.destination)

    UserRepository.create(visit.host)
    VisitorRepository.create(visit.visitor)

    DatabaseSession.commit()

    created = client.post(
        "/api/visits",
        json={
            "visitor_id": visit.visitor.id,
            "host_id": visit.host.id,
            "destination_id": visit.destination.id,
            "site_id": visit.site.id,
            "visit_type": visit.visit_type,
            "purpose": visit.purpose,
        },
        headers=auth_headers,
    ).get_json()["data"]

    response = client.get(
        f"/api/visits/{created['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_create_visit(client, session, auth_headers):

    visit = VisitFactory()

    OrganizationRepository.create(visit.host.organization)
    DepartmentRepository.create(visit.host.department)

    SiteRepository.create(visit.site)
    BuildingRepository.create(visit.destination.floor.building)
    FloorRepository.create(visit.destination.floor)
    DestinationRepository.create(visit.destination)

    UserRepository.create(visit.host)
    VisitorRepository.create(visit.visitor)

    DatabaseSession.commit()

    response = client.post(
        "/api/visits",
        json={
            "visitor_id": visit.visitor.id,
            "host_id": visit.host.id,
            "destination_id": visit.destination.id,
            "site_id": visit.site.id,
            "visit_type": visit.visit_type,
            "purpose": visit.purpose,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201


def test_delete_visit(client, session, auth_headers):

    visit = VisitFactory()

    OrganizationRepository.create(visit.host.organization)
    DepartmentRepository.create(visit.host.department)

    SiteRepository.create(visit.site)
    BuildingRepository.create(visit.destination.floor.building)
    FloorRepository.create(visit.destination.floor)
    DestinationRepository.create(visit.destination)

    UserRepository.create(visit.host)
    VisitorRepository.create(visit.visitor)

    DatabaseSession.commit()

    created = client.post(
        "/api/visits",
        json={
            "visitor_id": visit.visitor.id,
            "host_id": visit.host.id,
            "destination_id": visit.destination.id,
            "site_id": visit.site.id,
            "visit_type": visit.visit_type,
            "purpose": visit.purpose,
        },
        headers=auth_headers,
    ).get_json()["data"]

    response = client.delete(
        f"/api/visits/{created['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200