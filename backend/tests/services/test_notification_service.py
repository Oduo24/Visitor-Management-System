import pytest

from app.common.constants import (
    NotificationChannel,
    NotificationStatus,
    VisitNotificationEvent,
)
from app.common.database import DatabaseSession
from app.common.exceptions import NotFoundError

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
from app.repositories.visit_notification_repository import (
    VisitNotificationRepository,
)

from app.services.notification_service import (
    NotificationService,
)
from app.services.visit_service import (
    VisitService,
)

from tests.factories.destination_factory import (
    DestinationFactory,
)
from tests.factories.user_factory import (
    UserFactory,
)
from tests.factories.visitor_factory import (
    VisitorFactory,
)


class FakeEmailProvider:

    def send(
        self,
        recipient,
        subject,
        message,
    ):
        return "fake-email-message-id"


class FakeSMSProvider:

    def send(
        self,
        recipient,
        message,
    ):
        return "fake-sms-message-id"


class FailingEmailProvider:

    def send(
        self,
        recipient,
        subject,
        message,
    ):
        raise RuntimeError(
            "Email provider unavailable"
        )


class FailingSMSProvider:

    def send(
        self,
        recipient,
        message,
    ):
        raise RuntimeError(
            "SMS provider unavailable"
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

    return VisitService.create({
        "visitor_id": visitor.id,
        "host_id": host.id,
        "destination_id": destination.id,
        "site_id": site.id,
        "visit_type": "PREBOOKED",
        "purpose": "Notification test visit",
    })


def test_send_email_creates_sent_notification(
    session,
    monkeypatch,
):

    visit = seed_visit()

    monkeypatch.setattr(
        NotificationService,
        "email_provider",
        FakeEmailProvider(),
    )

    notification = (
        NotificationService.send_email(
            visit_id=visit.id,
            recipient="visitor@example.com",
            event=(
                VisitNotificationEvent
                .VISITOR_INVITED
            ),
            subject="Visitor Invitation",
            message="Complete your details.",
        )
    )

    assert notification.id is not None

    assert (
        notification.visit_id
        == visit.id
    )

    assert (
        notification.recipient
        == "visitor@example.com"
    )

    assert (
        notification.channel
        == NotificationChannel.EMAIL
    )

    assert (
        notification.event
        == (
            VisitNotificationEvent
            .VISITOR_INVITED
        )
    )

    assert (
        notification.status
        == NotificationStatus.SENT
    )

    assert (
        notification.subject
        == "Visitor Invitation"
    )

    assert (
        notification.message
        == "Complete your details."
    )

    assert notification.sent_at is not None

    assert (
        notification.provider_message_id
        == "fake-email-message-id"
    )

    assert notification.error_message is None


def test_send_sms_creates_sent_notification(
    session,
    monkeypatch,
):

    visit = seed_visit()

    monkeypatch.setattr(
        NotificationService,
        "sms_provider",
        FakeSMSProvider(),
    )

    notification = (
        NotificationService.send_sms(
            visit_id=visit.id,
            recipient="+254700000000",
            event=(
                VisitNotificationEvent
                .VISITOR_INVITED
            ),
            message="Your visitor invitation.",
        )
    )

    assert notification.id is not None

    assert (
        notification.visit_id
        == visit.id
    )

    assert (
        notification.recipient
        == "+254700000000"
    )

    assert (
        notification.channel
        == NotificationChannel.SMS
    )

    assert (
        notification.status
        == NotificationStatus.SENT
    )

    assert (
        notification.provider_message_id
        == "fake-sms-message-id"
    )

    assert notification.sent_at is not None

    assert notification.error_message is None


def test_send_email_records_provider_failure(
    session,
    monkeypatch,
):

    visit = seed_visit()

    monkeypatch.setattr(
        NotificationService,
        "email_provider",
        FailingEmailProvider(),
    )

    notification = (
        NotificationService.send_email(
            visit_id=visit.id,
            recipient="visitor@example.com",
            event=(
                VisitNotificationEvent
                .VISITOR_INVITED
            ),
            subject="Visitor Invitation",
            message="Complete your details.",
        )
    )

    assert notification.id is not None

    assert (
        notification.status
        == NotificationStatus.FAILED
    )

    assert notification.sent_at is None

    assert (
        notification.provider_message_id
        is None
    )

    assert (
        notification.error_message
        == "Email provider unavailable"
    )


def test_send_sms_records_provider_failure(
    session,
    monkeypatch,
):

    visit = seed_visit()

    monkeypatch.setattr(
        NotificationService,
        "sms_provider",
        FailingSMSProvider(),
    )

    notification = (
        NotificationService.send_sms(
            visit_id=visit.id,
            recipient="+254700000000",
            event=(
                VisitNotificationEvent
                .VISITOR_INVITED
            ),
            message="Complete your details.",
        )
    )

    assert notification.id is not None

    assert (
        notification.status
        == NotificationStatus.FAILED
    )

    assert notification.sent_at is None

    assert (
        notification.provider_message_id
        is None
    )

    assert (
        notification.error_message
        == "SMS provider unavailable"
    )


def test_send_email_visit_not_found(
    session,
    monkeypatch,
):

    monkeypatch.setattr(
        NotificationService,
        "email_provider",
        FakeEmailProvider(),
    )

    with pytest.raises(
        NotFoundError,
        match="Visit not found",
    ):
        NotificationService.send_email(
            visit_id=(
                "00000000-0000-0000-"
                "0000-000000000000"
            ),
            recipient="visitor@example.com",
            event=(
                VisitNotificationEvent
                .VISITOR_INVITED
            ),
            subject="Invitation",
            message="Message",
        )


def test_send_sms_visit_not_found(
    session,
    monkeypatch,
):

    monkeypatch.setattr(
        NotificationService,
        "sms_provider",
        FakeSMSProvider(),
    )

    with pytest.raises(
        NotFoundError,
        match="Visit not found",
    ):
        NotificationService.send_sms(
            visit_id=(
                "00000000-0000-0000-"
                "0000-000000000000"
            ),
            recipient="+254700000000",
            event=(
                VisitNotificationEvent
                .VISITOR_INVITED
            ),
            message="Message",
        )


def test_notification_history_by_visit(
    session,
    monkeypatch,
):

    visit = seed_visit()

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

    NotificationService.send_email(
        visit_id=visit.id,
        recipient="visitor@example.com",
        event=(
            VisitNotificationEvent
            .VISITOR_INVITED
        ),
        subject="Invitation",
        message="Email message",
    )

    NotificationService.send_sms(
        visit_id=visit.id,
        recipient="+254700000000",
        event=(
            VisitNotificationEvent
            .VISITOR_INVITED
        ),
        message="SMS message",
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
        for notification
        in notifications
    }

    assert channels == {
        NotificationChannel.EMAIL,
        NotificationChannel.SMS,
    }