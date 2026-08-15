import secrets
from datetime import datetime, timezone

from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError

from app.services.visit_service import VisitService


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

        DatabaseSession.commit()

        return visit