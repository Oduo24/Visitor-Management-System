import uuid

from app.common.database import DatabaseSession

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
from app.services.visit_invitation_service import (
    VisitInvitationService,
)

from tests.factories.user_factory import UserFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.destination_factory import (
    DestinationFactory,
)


def seed_visit():

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

    SiteRepository.create(site)

    BuildingRepository.create(
        destination.floor.building
    )

    FloorRepository.create(
        destination.floor
    )

    DestinationRepository.create(
        destination
    )

    UserRepository.create(host)
    VisitorRepository.create(visitor)

    DatabaseSession.flush()

    return VisitService.create({
        "visitor_id": visitor.id,
        "host_id": host.id,
        "destination_id": destination.id,
        "site_id": site.id,
        "visit_type": "PREBOOKED",
        "purpose": "Invitation API Test",
    })


def test_create_visit_invitation(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    response = client.post(
        f"/api/visits/{visit.id}/invitation",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["id"] is not None
    assert data["visit_id"] == str(
        visit.id
    )
    assert data["token"] is not None
    assert len(data["token"]) > 20
    assert data["expires_at"] is not None


def test_create_visit_invitation_not_found(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    response = client.post(
        f"/api/visits/{uuid.uuid4()}/invitation",
        headers=headers,
    )

    assert response.status_code == 404


def test_create_visit_invitation_requires_authentication(
    client,
    session,
):

    visit = seed_visit()

    response = client.post(
        f"/api/visits/{visit.id}/invitation"
    )

    assert response.status_code == 401


def test_create_visit_invitation_rejects_duplicate_active_invitation(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    first_response = client.post(
        f"/api/visits/{visit.id}/invitation",
        headers=headers,
    )

    assert first_response.status_code == 200

    second_response = client.post(
        f"/api/visits/{visit.id}/invitation",
        headers=headers,
    )

    assert second_response.status_code == 409


def test_get_visit_invitation(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    create_response = client.post(
        f"/api/visits/{visit.id}/invitation",
        headers=headers,
    )

    assert create_response.status_code == 200

    token = (
        create_response
        .get_json()["data"]["token"]
    )

    response = client.get(
        f"/api/visits/invitations/{token}"
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["visit_id"] == str(
        visit.id
    )
    assert data["expires_at"] is not None


def test_get_visit_invitation_not_found(
    client,
    session,
):

    response = client.get(
        "/api/visits/invitations/"
        "invalid-token"
    )

    assert response.status_code == 404