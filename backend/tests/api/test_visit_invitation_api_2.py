import uuid
import secrets
from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError

from app.services.visit_invitation_service import (
    VisitInvitationService,
)

from tests.factories.user_factory import UserFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.destination_factory import (
    DestinationFactory,
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


def test_get_visit_invitation(
    client,
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    response = client.get(
        f"/api/visits/invitations/"
        f"{invitation.token}"
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["visit_id"] == str(
        visit.id
    )

    assert data["site"] == (
        visit.site.name
    )

    assert data["host"] == (
        f"{visit.host.first_name} "
        f"{visit.host.last_name}"
    )

    assert data["visit_type"] == (
        visit.visit_type
    )

    assert data["purpose"] == (
        visit.purpose
    )

    assert data["visitor"]["first_name"] == (
        visit.visitor.first_name
    )

    assert data["visitor"]["last_name"] == (
        visit.visitor.last_name
    )

    assert data["expires_at"] is not None


def test_get_visit_invitation_not_found(
    client,
    session,
):

    token = secrets.token_urlsafe(32)

    response = client.get(
        f"/api/visits/invitations/{token}"
    )

    assert response.status_code == 404


def test_get_visit_invitation_completed(
    client,
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    VisitInvitationService.complete(
        invitation.token,
        {},
    )

    response = client.get(
        f"/api/visits/invitations/"
        f"{invitation.token}"
    )

    assert response.status_code == 409


def test_patch_visit_invitation(
    client,
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    response = client.patch(
        f"/api/visits/invitations/"
        f"{invitation.token}",
        json={
            "first_name": "Updated",
            "middle_name": "Visitor",
            "last_name": "Name",
            "phone": "0712345678",
            "email": "visitor@example.com",
            "id_number": "12345678",
        },
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["visit_id"] == str(
        visit.id
    )

    assert data["completed"] is True

    assert (
        visit.visitor.first_name
        == "Updated"
    )

    assert (
        visit.visitor.middle_name
        == "Visitor"
    )

    assert (
        visit.visitor.last_name
        == "Name"
    )

    assert (
        visit.visitor.phone
        == "0712345678"
    )

    assert (
        visit.visitor.email
        == "visitor@example.com"
    )

    assert (
        visit.visitor.id_number
        == "12345678"
    )


def test_patch_visit_invitation_partial_update(
    client,
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    original_last_name = (
        visit.visitor.last_name
    )

    response = client.patch(
        f"/api/visits/invitations/"
        f"{invitation.token}",
        json={
            "phone": "0798765432",
        },
    )

    assert response.status_code == 200

    assert (
        visit.visitor.phone
        == "0798765432"
    )

    assert (
        visit.visitor.last_name
        == original_last_name
    )


def test_patch_visit_invitation_not_found(
    client,
    session,
):

    token = secrets.token_urlsafe(32)

    response = client.patch(
        f"/api/visits/invitations/{token}",
        json={
            "first_name": "Updated",
        },
    )

    assert response.status_code == 404


def test_patch_visit_invitation_cannot_be_completed_twice(
    client,
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    first_response = client.patch(
        f"/api/visits/invitations/"
        f"{invitation.token}",
        json={
            "first_name": "First Update",
        },
    )

    assert first_response.status_code == 200

    second_response = client.patch(
        f"/api/visits/invitations/"
        f"{invitation.token}",
        json={
            "first_name": "Second Update",
        },
    )

    assert second_response.status_code == 409

    data = second_response.get_json()

    assert data["success"] is False


def test_get_visit_invitation_does_not_require_authentication(
    client,
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    response = client.get(
        f"/api/visits/invitations/"
        f"{invitation.token}"
    )

    assert response.status_code == 200


def test_patch_visit_invitation_does_not_require_authentication(
    client,
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    response = client.patch(
        f"/api/visits/invitations/"
        f"{invitation.token}",
        json={
            "first_name": "Updated",
        },
    )

    assert response.status_code == 200