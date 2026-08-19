from datetime import datetime, timedelta, timezone

import pytest

from app.common.database import DatabaseSession
from app.common.exceptions import (
    ConflictError,
    NotFoundError,
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

from app.models.visit_invitation import VisitInvitation

from app.services.visit_service import VisitService
from app.services.visit_invitation_service import (
    VisitInvitationService,
)

from app.repositories.visit_invitation_repository import VisitInvitationRepository
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

    visit = VisitService.create({
        "visitor_id": visitor.id,
        "host_id": host.id,
        "destination_id": destination.id,
        "site_id": site.id,
        "visit_type": "PREBOOKED",
        "purpose": "Invitation Test",
    })

    return visit


def test_create_invitation(session):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    assert invitation.id is not None
    assert invitation.visit_id == visit.id
    assert invitation.token is not None
    assert len(invitation.token) > 20
    assert invitation.expires_at is not None
    assert invitation.used_at is None


def test_create_invitation_has_expiry(
    session,
):

    visit = seed_visit()

    before = (
        datetime.now(timezone.utc).replace(tzinfo=None)
        + timedelta(hours=47)
    )

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    after = (
        datetime.now(timezone.utc).replace(tzinfo=None)
        + timedelta(hours=49)
    )

    assert (
        before
        <= invitation.expires_at
        <= after
    )


def test_create_invitation_with_custom_expiry(
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id,
            expiry_hours=24,
        )
    )

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    expected_min = (
        now + timedelta(hours=23)
    )

    expected_max = (
        now + timedelta(hours=25)
    )

    assert (
        expected_min
        <= invitation.expires_at
        <= expected_max
    )


def test_create_invitation_rejects_existing_active_invitation(
    session,
):

    visit = seed_visit()

    VisitInvitationService.create(
        visit.id
    )

    with pytest.raises(
        ConflictError,
        match="active invitation",
    ):
        VisitInvitationService.create(
            visit.id
        )


def test_create_invitation_allows_new_invitation_after_previous_used(
    session,
):

    visit = seed_visit()

    first = (
        VisitInvitationService.create(
            visit.id
        )
    )

    VisitInvitationService.use(
        first.token
    )

    second = (
        VisitInvitationService.create(
            visit.id
        )
    )

    assert second.id is not None
    assert second.id != first.id
    assert second.token != first.token


def test_get_invitation_by_token(
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    found = (
        VisitInvitationService
        .get_by_token(
            invitation.token
        )
    )

    assert found.id == invitation.id
    assert found.visit_id == visit.id
    assert found.token == invitation.token


def test_get_invitation_not_found(
    session,
):

    with pytest.raises(
        NotFoundError,
        match="Invitation not found",
    ):
        VisitInvitationService.get_by_token(
            "invalid-token"
        )


def test_get_expired_invitation(
    session,
):

    visit = seed_visit()

    invitation = VisitInvitation(
        visit_id=visit.id,
        token="expired-test-token",
        expires_at=(
            datetime.now(
                timezone.utc
            ).replace(
                tzinfo=None
            )
            - timedelta(hours=1)
        ),
    )

    VisitInvitationRepository.create(
        invitation
    )

    DatabaseSession.commit()

    with pytest.raises(
        ConflictError,
        match="expired",
    ):
        VisitInvitationService.get_by_token(
            invitation.token
        )


def test_get_used_invitation(
    session,
):

    visit = seed_visit()

    invitation = VisitInvitation(
        visit_id=visit.id,
        token="used-test-token",
        expires_at=(
            datetime.now(timezone.utc)
            + timedelta(hours=24)
        ),
        used_at=datetime.now(timezone.utc),
    )

    VisitInvitationRepository.create(
        invitation
    )

    DatabaseSession.commit()

    with pytest.raises(
        ConflictError,
        match="already been used",
    ):
        VisitInvitationService.get_by_token(
            invitation.token
        )


def test_use_invitation(
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    assert invitation.used_at is None

    used = (
        VisitInvitationService.use(
            invitation.token
        )
    )

    assert used.id == invitation.id
    assert used.used_at is not None


def test_use_invitation_cannot_be_used_twice(
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    VisitInvitationService.use(
        invitation.token
    )

    with pytest.raises(
        ConflictError,
        match="already been used",
    ):
        VisitInvitationService.use(
            invitation.token
        )