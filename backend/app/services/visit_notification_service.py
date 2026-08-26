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
 
 
class VisitNotificationService:
 
    @staticmethod
    def _frontend_base_url():
 
        return current_app.config.get(
            "FRONTEND_BASE_URL",
            "http://localhost:5173",
        ).rstrip("/")
 
 
    @staticmethod
    def send_registration_invitation(
        visit_id,
        invitation_token,
    ):
 
        visit = VisitService.get_by_id(
            visit_id
        )
 
        visitor = visit.visitor
 
        base_url = (
            VisitNotificationService
            ._frontend_base_url()
        )
 
        invitation_url = (
            f"{base_url}"
            f"/invitations/"
            f"{invitation_token}"
        )
 
        notifications = []
 
 
        # EMAIL
        if visitor.email:
 
            subject = (
                "Complete Your Visitor Registration"
            )
 
            message = (
                f"Hello {visitor.first_name},\n\n"
 
                "A visit has been scheduled "
                "for you.\n\n"
 
                f"Host: "
                f"{visit.host.first_name} "
                f"{visit.host.last_name}\n"
 
                f"Site: "
                f"{visit.site.name}\n"
 
                f"Purpose: "
                f"{visit.purpose or '-'}\n"
 
                f"Expected arrival: "
                f"{visit.expected_arrival or '-'}\n\n"
 
                "Please complete or confirm "
                "your visitor details using "
                "the link below:\n\n"
 
                f"{invitation_url}\n\n"
 
                "Your official visitor pass "
                "will be sent separately once "
                "your registration is complete "
                "and the visit has been approved."
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
 
 
        # SMS
        if visitor.phone:
 
            message = (
                f"Hello {visitor.first_name}. "
                "A visit has been scheduled "
                f"with {visit.host.first_name} "
                f"{visit.host.last_name} "
                f"at {visit.site.name}. "
 
                "Please complete your visitor "
                "registration: "
                f"{invitation_url}. "
 
                "Your official visitor pass "
                "will be sent after approval."
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
 
 
    @staticmethod
    def send_official_invitation(
        visit_id,
        access_pass_token,
    ):
 
        visit = VisitService.get_by_id(
            visit_id
        )
 
        visitor = visit.visitor
 
 
        if not visit.visitor_code:
 
            raise ConflictError(
                "Visitor code has not been generated."
            )
 
 
        if not visit.qr_token:
 
            raise ConflictError(
                "QR code has not been generated."
            )
 
 
        if not access_pass_token:
 
            raise ConflictError(
                "Access pass token is required."
            )
 
 
        base_url = (
            VisitNotificationService
            ._frontend_base_url()
        )
 
 
        pass_url = (
            f"{base_url}"
            f"/visitor-pass/"
            f"{access_pass_token}"
        )
 
 
        notifications = []
 
 
        # EMAIL
        if visitor.email:
 
            subject = (
                "Your Official Visitor Pass"
            )
 
            message = (
                f"Hello {visitor.first_name},\n\n"
 
                "Your visit is confirmed and "
                "your official visitor pass "
                "is now ready.\n\n"
 
                f"Visitor Code: "
                f"{visit.visitor_code}\n\n"
 
                f"Host: "
                f"{visit.host.first_name} "
                f"{visit.host.last_name}\n"
 
                f"Site: "
                f"{visit.site.name}\n"
 
                f"Purpose: "
                f"{visit.purpose or '-'}\n"
 
                f"Expected arrival: "
                f"{visit.expected_arrival or '-'}\n\n"
 
                "Open your digital visitor "
                "pass using the link below:\n\n"
 
                f"{pass_url}\n\n"
 
                "The digital pass contains "
                "your visit details, visitor "
                "code and QR code. Please "
                "present it at reception."
            )
 
            notifications.append(
                NotificationService.send_email(
                    visit_id=visit.id,
                    recipient=visitor.email,
                    event=(
                        VisitNotificationEvent
                        .VISITOR_PASS_ISSUED
                    ),
                    subject=subject,
                    message=message,
                )
            )
 
 
        # SMS
        if visitor.phone:
 
            message = (
                f"Hello {visitor.first_name}. "
 
                "Your visit has been approved. "
 
                f"Visitor Code: "
                f"{visit.visitor_code}. "
 
                "Open your official visitor "
                "pass with visit details and "
                "QR code: "
                f"{pass_url}"
            )
 
            notifications.append(
                NotificationService.send_sms(
                    visit_id=visit.id,
                    recipient=visitor.phone,
                    event=(
                        VisitNotificationEvent
                        .VISITOR_PASS_ISSUED
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