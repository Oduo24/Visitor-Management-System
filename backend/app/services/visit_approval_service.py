from datetime import datetime, timezone

from flask_jwt_extended import get_jwt_identity

from app.common.database import DatabaseSession
from app.common.constants import VisitStatus
from app.common.exceptions import ConflictError

from app.services.visit_service import VisitService


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

        visit.status = (
            VisitStatus.APPROVED
            if approved
            else VisitStatus.REJECTED
        )

        visit.approved_by = get_jwt_identity()

        visit.approved_at = datetime.now(timezone.utc)

        if notes:
            visit.notes = notes

        DatabaseSession.commit()

        return visit