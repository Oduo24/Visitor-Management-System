from datetime import datetime, timezone

from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError

from app.common.constants import VisitAuditAction, VisitStatus

from app.services.visit_service import VisitService
from app.services.visit_audit_service import VisitAuditService

class VisitCheckoutService:

    @staticmethod
    def check_out(visit_id):

        visit = VisitService.get_by_id(
            visit_id
        )

        if visit.status != VisitStatus.CHECKED_IN:
            raise ConflictError(
                "Only checked-in visits can be checked out."
            )

        if not visit.checked_in_at:
            raise ConflictError(
                "Visit has not been checked in."
            )

        if visit.checked_out_at:
            raise ConflictError(
                "Visit has already been checked out."
            )

        visit.status = VisitStatus.CHECKED_OUT

        visit.checked_out_at = datetime.now(
            timezone.utc
        )

        VisitAuditService.create(
        visit_id=visit.id,
        action=VisitAuditAction.CHECKED_OUT,
        )

        DatabaseSession.commit()

        return visit