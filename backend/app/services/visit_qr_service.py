import secrets
from datetime import datetime, timezone

from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError

from app.services.visit_service import VisitService
from app.common.constants import VisitAuditAction
from app.services.visit_audit_service import VisitAuditService
from app.repositories.visit_repository import VisitRepository


class VisitQRService:

    @staticmethod
    def generate(visit_id):

        visit = VisitService.get_by_id(
            visit_id
        )

        if visit.qr_token:
            raise ConflictError(
                "QR code has already been generated."
            )

        visit.qr_token = secrets.token_urlsafe(32)

        visit.qr_generated_at = datetime.now(
            timezone.utc
        )

        VisitAuditService.create(
        visit_id=visit.id,
        action=VisitAuditAction.QR_GENERATED,
        )

        DatabaseSession.commit()

        return visit

    @staticmethod
    def validate(token):

        if not token:
            raise ConflictError(
                "QR token is required."
            )
    
        visit = (
            VisitRepository
            .get_by_qr_token(token)
        )

        if not visit:
            raise NotFoundError(
                "Invalid QR token."
            )

        if not visit.qr_token:
            raise NotFoundError(
                "Invalid QR token."
            )

        return visit