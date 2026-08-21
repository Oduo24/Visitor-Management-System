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

from app.common.constants import (
    NotificationChannel,
    NotificationStatus,
    VisitNotificationEvent,
)
 
from app.repositories.visit_notification_repository import (
    VisitNotificationRepository,
)
 
from app.services.notification_service import (
    NotificationService,
)

class FakeEmailProvider:
 
    def send(
        self,
        recipient,
        subject,
        message,
    ):
        return "automatic-email-id"
 
class FakeSMSProvider:
 
    def send(
        self,
        recipient,
        message,
    ):
        return "automatic-sms-id"
 
 
class FailingEmailProvider:
 
    def send(
        self,
        recipient,
        subject,
        message,
    ):
        raise RuntimeError(
            "Email unavailable"
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
    assert invitation.completed_at is None


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


def test_create_invitation_allows_new_invitation_after_previous_completed(
    session,
):

    visit = seed_visit()

    first = (
        VisitInvitationService.create(
            visit.id
        )
    )

    VisitInvitationService.complete(
        first.token,
        {},
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


def test_get_completed_invitation(
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
        completed_at=datetime.now(timezone.utc),
    )

    VisitInvitationRepository.create(
        invitation
    )

    DatabaseSession.commit()

    with pytest.raises(
        ConflictError,
        match="already been completed",
    ):
        VisitInvitationService.get_by_token(
            invitation.token
        )


def test_complete_invitation(
    session,
):

    visit = seed_visit()

    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )

    assert invitation.completed_at is None

    completed = (
        VisitInvitationService.complete(
            invitation.token,
            {},
        )
    )

    assert completed.completed_at is not None


def test_use_invitation_cannot_be_used_twice(
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

    with pytest.raises(
        ConflictError,
        match="Invitation has already been completed.",
    ):
        VisitInvitationService.complete(
            invitation.token,
            {},
        )



def test_create_invitation_automatically_sends_email_and_sms(
    session,
    monkeypatch,
):
 
    monkeypatch.setattr(
        NotificationService,
        "email_provider",
        FakeEmailProvider(),
    )
 
    monkeypatch.setattr(
        NotificationService,
        "sms_provider",
        FakeSMSProvider(),
    )
 
    visit = seed_visit()
 
    visit.visitor.email = (
        "visitor@example.com"
    )
 
    visit.visitor.phone = (
        "+254700000000"
    )
 
    DatabaseSession.commit()
 
    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )
 
    notifications = (
        VisitNotificationRepository
        .get_by_visit_id(
            visit.id
        )
    )
 
    assert len(notifications) == 2
 
    channels = {
        notification.channel
        for notification in notifications
    }
 
    assert channels == {
        NotificationChannel.EMAIL,
        NotificationChannel.SMS,
    }
 
    assert all(
        notification.event
        == (
            VisitNotificationEvent
            .VISITOR_INVITED
        )
        for notification in notifications
    )
 
    assert all(
        notification.status
        == NotificationStatus.SENT
        for notification in notifications
    )
 
    assert all(
        invitation.token
        in notification.message
        for notification in notifications
    )


def test_create_invitation_automatically_sends_email_only(
    session,
    monkeypatch,
):
 
    monkeypatch.setattr(
        NotificationService,
        "email_provider",
        FakeEmailProvider(),
    )
 
    monkeypatch.setattr(
        NotificationService,
        "sms_provider",
        FakeSMSProvider(),
    )
 
    visit = seed_visit()
 
    visit.visitor.email = (
        "visitor@example.com"
    )
 
    visit.visitor.phone = None
 
    DatabaseSession.commit()
 
    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )
 
    notifications = (
        VisitNotificationRepository
        .get_by_visit_id(
            visit.id
        )
    )
 
    assert len(notifications) == 1
 
    notification = notifications[0]
 
    assert (
        notification.channel
        == NotificationChannel.EMAIL
    )
 
    assert (
        notification.recipient
        == "visitor@example.com"
    )
 
    assert (
        notification.status
        == NotificationStatus.SENT
    )
 
    assert (
        invitation.token
        in notification.message
    )


def test_create_invitation_automatically_sends_sms_only(
    session,
    monkeypatch,
):
 
    monkeypatch.setattr(
        NotificationService,
        "email_provider",
        FakeEmailProvider(),
    )
 
    monkeypatch.setattr(
        NotificationService,
        "sms_provider",
        FakeSMSProvider(),
    )
 
    visit = seed_visit()
 
    visit.visitor.email = None
 
    visit.visitor.phone = (
        "+254711111111"
    )
 
    DatabaseSession.commit()
 
    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )
 
    notifications = (
        VisitNotificationRepository
        .get_by_visit_id(
            visit.id
        )
    )
 
    assert len(notifications) == 1
 
    notification = notifications[0]
 
    assert (
        notification.channel
        == NotificationChannel.SMS
    )
 
    assert (
        notification.recipient
        == "+254711111111"
    )
 
    assert (
        notification.status
        == NotificationStatus.SENT
    )
 
    assert (
        invitation.token
        in notification.message
    )


def test_create_invitation_without_contact_details_still_succeeds(
    session,
    monkeypatch,
):
 
    monkeypatch.setattr(
        NotificationService,
        "email_provider",
        FakeEmailProvider(),
    )
 
    monkeypatch.setattr(
        NotificationService,
        "sms_provider",
        FakeSMSProvider(),
    )
 
    visit = seed_visit()
 
    visit.visitor.email = None
    visit.visitor.phone = None
 
    DatabaseSession.commit()
 
    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )
 
    assert invitation.id is not None
    assert invitation.token is not None
 
    notifications = (
        VisitNotificationRepository
        .get_by_visit_id(
            visit.id
        )
    )
 
    assert notifications == []


def test_create_invitation_survives_notification_failure(
    session,
    monkeypatch,
):
 
    monkeypatch.setattr(
        NotificationService,
        "email_provider",
        FailingEmailProvider(),
    )
 
    visit = seed_visit()
 
    visit.visitor.email = (
        "visitor@example.com"
    )
 
    visit.visitor.phone = None
 
    DatabaseSession.commit()
 
    invitation = (
        VisitInvitationService.create(
            visit.id
        )
    )
 
    assert invitation.id is not None
 
    notifications = (
        VisitNotificationRepository
        .get_by_visit_id(
            visit.id
        )
    )
 
    assert len(notifications) == 1
 
    notification = notifications[0]
 
    assert (
        notification.channel
        == NotificationChannel.EMAIL
    )
 
    assert (
        notification.status
        == NotificationStatus.FAILED
    )
 
    assert (
        notification.error_message
        == "Email unavailable"
    )
 
    assert notification.sent_at is None