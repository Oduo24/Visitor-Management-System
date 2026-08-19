from datetime import datetime, timezone

from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError

from app.common.constants import VisitAuditAction, VisitStatus

from app.services.visit_service import VisitService
from app.services.visit_audit_service import VisitAuditService

class VisitCheckinService:

    @staticmethod
    def check_in(visit_id):

        visit = VisitService.get_by_id(
            visit_id
        )

        if visit.status != VisitStatus.APPROVED:
            raise ConflictError(
                "Only approved visits can be checked in."
            )

        if not visit.badge_number:
            raise ConflictError(
                "A badge must be issued before check-in."
            )

        if visit.checked_in_at:
            raise ConflictError(
                "Visit has already been checked in."
            )

        visit.status = VisitStatus.CHECKED_IN

        visit.checked_in_at = datetime.now(
            timezone.utc
        )

        visit.status = VisitStatus.CHECKED_IN

        visit.checked_in_at = datetime.now(
            timezone.utc
        )
    
        VisitAuditService.create(
            visit_id=visit.id,
            action=VisitAuditAction.CHECKED_IN,
        )

        DatabaseSession.commit()

        return visit