from flask import current_app

from app.common.constants import (
    VisitNotificationEvent,
)

from app.common.exceptions import (
    ConflictError,
)

from app.services.notification_service import (
    NotificationService,
)

from app.services.visit_service import (
    VisitService,
)

from app.repositories.visit_invitation_repository import (
    VisitInvitationRepository,
)


class VisitNotificationService:

    @staticmethod
    def send_visitor_invitation(
        visit_id,
        invitation_token,
    ):

        visit = VisitService.get_by_id(
            visit_id
        )

        visitor = visit.visitor

        base_url = current_app.config.get(
            "FRONTEND_BASE_URL",
            "http://localhost:5173",
        )

        invitation_url = (
            f"{base_url}/invitation/"
            f"{invitation_token}"
        )

        notifications = []

        if visitor.email:

            subject = (
                "Visitor Invitation"
            )

            message = (
                f"Hello {visitor.first_name},\n\n"
                "Your visit has been scheduled.\n\n"
                f"Host: {visit.host.first_name}\n"
                f"Site: {visit.site.name}\n"
                f"Purpose: {visit.purpose or '-'}\n\n"
                f"Visitor Code: {visit.visitor_code}\n\n"
                "Please complete your visitor "
                "details using the link below:\n\n"
                f"{invitation_url}\n"
            )

            notifications.append(
                NotificationService.send_email(
                    visit_id=visit.id,
                    recipient=visitor.email,
                    event=(
                        VisitNotificationEvent
                        .VISITOR_INVITED
                    ),
                    subject=subject,
                    message=message,
                )
            )

        if visitor.phone:

            message = (
                f"Hello {visitor.first_name}. "
                "Your visit has been scheduled. "
                f"Visitor Code: "
                f"{visit.visitor_code}. "
                "Complete your visitor details: "
                f"{invitation_url}"
            )

            notifications.append(
                NotificationService.send_sms(
                    visit_id=visit.id,
                    recipient=visitor.phone,
                    event=(
                        VisitNotificationEvent
                        .VISITOR_INVITED
                    ),
                    message=message,
                )
            )

        if not notifications:

            raise ConflictError(
                "Visitor has no email address "
                "or phone number."
            )

        return notifications