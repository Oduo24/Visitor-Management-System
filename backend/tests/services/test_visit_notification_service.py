import pytest

from app.common.constants import (
    NotificationChannel,
    NotificationStatus,
    VisitNotificationEvent,
)
from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError

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
from app.services.visit_notification_service import (
    VisitNotificationService,
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
        return "visitor-email-id"


class FakeSMSProvider:

    def send(
        self,
        recipient,
        message,
    ):
        return "visitor-sms-id"


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
        "purpose": "Business Meeting",
    })


def configure_providers(
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


def test_send_visitor_invitation_email_and_sms(
    app,
    session,
    monkeypatch,
):

    configure_providers(
        monkeypatch
    )

    monkeypatch.setitem(
        app.config,
        "FRONTEND_BASE_URL",
        "http://frontend.test",
    )

    visit = seed_visit()

    visit.visitor.email = (
        "visitor@example.com"
    )

    visit.visitor.phone = (
        "+254700000000"
    )

    DatabaseSession.commit()

    notifications = (
        VisitNotificationService
        .send_visitor_invitation(
            visit_id=visit.id,
            invitation_token=(
                "secure-invitation-token"
            ),
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

    for notification in notifications:

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
            "secure-invitation-token"
            in notification.message
        )

        assert (
            "http://frontend.test"
            in notification.message
        )


def test_send_visitor_invitation_email_only(
    app,
    session,
    monkeypatch,
):

    configure_providers(
        monkeypatch
    )

    visit = seed_visit()

    visit.visitor.email = (
        "visitor@example.com"
    )

    visit.visitor.phone = None

    DatabaseSession.commit()

    notifications = (
        VisitNotificationService
        .send_visitor_invitation(
            visit.id,
            "email-only-token",
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
        "email-only-token"
        in notification.message
    )


def test_send_visitor_invitation_sms_only(
    app,
    session,
    monkeypatch,
):

    configure_providers(
        monkeypatch
    )

    visit = seed_visit()

    visit.visitor.email = None

    visit.visitor.phone = (
        "+254711111111"
    )

    DatabaseSession.commit()

    notifications = (
        VisitNotificationService
        .send_visitor_invitation(
            visit.id,
            "sms-only-token",
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
        "sms-only-token"
        in notification.message
    )


def test_send_visitor_invitation_without_contact_details(
    app,
    session,
    monkeypatch,
):

    configure_providers(
        monkeypatch
    )

    visit = seed_visit()

    visit.visitor.email = None
    visit.visitor.phone = None

    DatabaseSession.commit()

    with pytest.raises(
        ConflictError,
        match="no email address or phone number",
    ):
        (
            VisitNotificationService
            .send_visitor_invitation(
                visit.id,
                "unused-token",
            )
        )


def test_send_visitor_invitation_persists_notifications(
    app,
    session,
    monkeypatch,
):

    configure_providers(
        monkeypatch
    )

    visit = seed_visit()

    visit.visitor.email = (
        "visitor@example.com"
    )

    visit.visitor.phone = (
        "+254722222222"
    )

    DatabaseSession.commit()

    (
        VisitNotificationService
        .send_visitor_invitation(
            visit.id,
            "history-token",
        )
    )

    stored = (
        VisitNotificationRepository
        .get_by_visit_id(
            visit.id
        )
    )

    assert len(stored) == 2

    assert all(
        notification.status
        == NotificationStatus.SENT
        for notification in stored
    )

    assert all(
        notification.event
        == (
            VisitNotificationEvent
            .VISITOR_INVITED
        )
        for notification in stored
    )


def test_invitation_email_contains_visit_information(
    app,
    session,
    monkeypatch,
):

    configure_providers(
        monkeypatch
    )

    visit = seed_visit()

    visit.visitor.email = (
        "visitor@example.com"
    )

    visit.visitor.phone = None

    DatabaseSession.commit()

    notifications = (
        VisitNotificationService
        .send_visitor_invitation(
            visit.id,
            "visit-info-token",
        )
    )

    email = notifications[0]

    assert (
        visit.visitor.first_name
        in email.message
    )

    assert (
        visit.site.name
        in email.message
    )

    assert (
        visit.purpose
        in email.message
    )

    assert (
        "visit-info-token"
        in email.message
    )