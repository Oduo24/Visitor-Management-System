import secrets
from datetime import datetime, timezone
 
from app.common.database import DatabaseSession
from app.common.exceptions import NotFoundError
from app.common.constants import VisitStatus, NotificationStatus
 
from app.repositories.visit_invitation_repository import (
    VisitInvitationRepository,
)
from app.repositories.visit_repository import (
    VisitRepository,
)
 
from app.services.visit_service import (
    VisitService,
)
from app.services.visit_code_service import (
    VisitCodeService,
)
from app.services.visit_qr_service import (
    VisitQRService,
)
from app.services.visit_notification_service import (
    VisitNotificationService,
)
 
 
class VisitAccessPassService:
 
    @staticmethod
    def _utc_now():
        return datetime.now(
            timezone.utc
        ).replace(
            tzinfo=None
        )
 
    @staticmethod
    def registration_completed(
        visit_id,
    ):
        invitations = (
            VisitInvitationRepository
            .get_by_visit_id(
                visit_id
            )
        )
 
        return any(
            invitation.completed_at
            is not None
            for invitation in invitations
        )
 
    @staticmethod
    def finalize_if_ready(
        visit_id,
    ):
        """
        Issue the official visitor pass only when:
 
        1. visitor registration is complete
        2. visit has been approved
        """
 
        visit = VisitService.get_by_id(
            visit_id
        )
 
        if (
            visit.status
            != VisitStatus.APPROVED
        ):
            return visit
 
        if not (
            VisitAccessPassService
            .registration_completed(
                visit.id
            )
        ):
            return visit
 
        # Visitor reception code
        VisitCodeService.ensure_code(
            visit.id
        )
 
        # QR scanning credential
        if not visit.qr_token:
            VisitQRService.generate(
                visit.id
            )
 
        # Public digital-pass token
        if not visit.access_pass_token:
 
            visit.access_pass_token = (
                secrets.token_urlsafe(
                    32
                )
            )
 
            visit.access_pass_generated_at = (
                VisitAccessPassService
                ._utc_now()
            )
 
            DatabaseSession.commit()
 
        # Never intentionally send the
        # official invitation twice.
        if (
            visit.official_invitation_sent_at
        ):
            return visit
 
        notifications = (
            VisitNotificationService
            .send_official_invitation(
                visit_id=visit.id,
                access_pass_token=(
                    visit.access_pass_token
                ),
            )
        )
        
        
        sent_successfully = any(
            notification.status
            == NotificationStatus.SENT
            for notification in notifications
        )
        
        
        if sent_successfully:
        
            visit.official_invitation_sent_at = (
                VisitAccessPassService
                ._utc_now()
            )
        
            DatabaseSession.commit()
 
        return visit
 
    @staticmethod
    def get_public_details(
        token,
    ):
 
        if not token:
            raise NotFoundError(
                "Visitor pass not found."
            )
 
        visit = (
            VisitRepository
            .get_by_access_pass_token(
                token
            )
        )
 
        if not visit:
            raise NotFoundError(
                "Visitor pass not found."
            )
 
        visitor = visit.visitor
 
        return {
            "visit_id": visit.id,
 
            "visitor_name": (
                visitor.full_name
            ),
 
            "company": (
                visitor.company
            ),
 
            "vehicle_registration": (
                visitor.vehicle_registration
            ),
 
            "visitor_code": (
                visit.visitor_code
            ),
 
            "host": (
                f"{visit.host.first_name} "
                f"{visit.host.last_name}"
            ),
 
            "site": (
                visit.site.name
            ),
 
            "destination": (
                visit.destination.name
                if visit.destination
                else None
            ),
 
            "visit_type": (
                visit.visit_type
            ),
 
            "status": (
                visit.status
            ),
 
            "purpose": (
                visit.purpose
            ),
 
            "expected_arrival": (
                visit.expected_arrival
            ),
 
            "expected_departure": (
                visit.expected_departure
            ),
 
            "qr_token": (
                visit.qr_token
            ),
 
            "pass_generated_at": (
                visit.access_pass_generated_at
            ),
        }


