from datetime import datetime, timezone

from app.common.constants import (
    NotificationChannel,
    NotificationStatus,
)

from app.common.database import (
    DatabaseSession,
)

from app.common.exceptions import (
    NotFoundError,
)

from app.models.visit_notification import (
    VisitNotification,
)

from app.repositories.visit_repository import (
    VisitRepository,
)

from app.repositories.visit_notification_repository import (
    VisitNotificationRepository,
)

from app.notifications.providers.console_email_provider import (
    ConsoleEmailProvider,
)

from app.notifications.providers.console_sms_provider import (
    ConsoleSMSProvider,
)


class NotificationService:

    email_provider = ConsoleEmailProvider()

    sms_provider = ConsoleSMSProvider()

    @staticmethod
    def _utc_now():

        return datetime.now(
            timezone.utc
        ).replace(
            tzinfo=None
        )

    @staticmethod
    def send_email(
        visit_id,
        recipient,
        event,
        subject,
        message,
    ):

        visit = VisitRepository.get_by_id(
            visit_id
        )

        if not visit:
            raise NotFoundError(
                "Visit not found."
            )

        notification = VisitNotification(
            visit_id=visit.id,
            recipient=recipient,
            channel=NotificationChannel.EMAIL,
            event=event,
            status=NotificationStatus.PENDING,
            subject=subject,
            message=message,
        )

        VisitNotificationRepository.create(
            notification
        )

        DatabaseSession.flush()

        try:

            provider_message_id = (
                NotificationService
                .email_provider
                .send(
                    recipient,
                    subject,
                    message,
                )
            )

            notification.status = (
                NotificationStatus.SENT
            )

            notification.sent_at = (
                NotificationService
                ._utc_now()
            )

            notification.provider_message_id = (
                provider_message_id
            )

        except Exception as exc:

            notification.status = (
                NotificationStatus.FAILED
            )

            notification.error_message = str(
                exc
            )

        DatabaseSession.commit()

        return notification

    @staticmethod
    def send_sms(
        visit_id,
        recipient,
        event,
        message,
    ):

        visit = VisitRepository.get_by_id(
            visit_id
        )

        if not visit:
            raise NotFoundError(
                "Visit not found."
            )

        notification = VisitNotification(
            visit_id=visit.id,
            recipient=recipient,
            channel=NotificationChannel.SMS,
            event=event,
            status=NotificationStatus.PENDING,
            message=message,
        )

        VisitNotificationRepository.create(
            notification
        )

        DatabaseSession.flush()

        try:

            provider_message_id = (
                NotificationService
                .sms_provider
                .send(
                    recipient,
                    message,
                )
            )

            notification.status = (
                NotificationStatus.SENT
            )

            notification.sent_at = (
                NotificationService
                ._utc_now()
            )

            notification.provider_message_id = (
                provider_message_id
            )

        except Exception as exc:

            notification.status = (
                NotificationStatus.FAILED
            )

            notification.error_message = str(
                exc
            )

        DatabaseSession.commit()

        return notification