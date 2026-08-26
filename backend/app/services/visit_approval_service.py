from datetime import datetime, timezone

from flask_jwt_extended import get_jwt_identity

from app.common.database import DatabaseSession
from app.common.constants import (
    VisitAuditAction,
    VisitStatus,
)
from app.common.exceptions import ConflictError

from app.services.visit_service import VisitService
from app.services.visit_audit_service import (
    VisitAuditService,
)

from app.services.visit_access_pass_service import (
    VisitAccessPassService,
)
from app.models import visit


class VisitApprovalService:

    @staticmethod
    def approve(
        visit_id,
        approved,
        notes=None,
    ):

        visit = VisitService.get_by_id(
            visit_id
        )

        if visit.status != VisitStatus.PENDING:
            raise ConflictError(
                "Visit has already been processed."
            )

        user_id = get_jwt_identity()

        now = datetime.now(
            timezone.utc
        ).replace(tzinfo=None)


        if approved:

            visit.status = (
                VisitStatus.APPROVED
            )

            visit.approved_by = user_id
            visit.approved_at = now

            visit.rejected_by = None
            visit.rejected_at = None

        else:

            visit.status = (
                VisitStatus.REJECTED
            )

            visit.rejected_by = user_id
            visit.rejected_at = now

            visit.approved_by = None
            visit.approved_at = None


        if notes:
            visit.notes = notes


        VisitAuditService.create(
            visit_id=visit.id,
            action=(
                VisitAuditAction.APPROVED
                if approved
                else VisitAuditAction.REJECTED
            ),
            notes=notes,
        )


        DatabaseSession.commit()

        if approved:
            VisitAccessPassService.finalize_if_ready(
                visit.id
            )
    
        return visit