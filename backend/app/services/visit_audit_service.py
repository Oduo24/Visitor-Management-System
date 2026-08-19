from app.common.exceptions import NotFoundError

from app.models.visit_audit import VisitAudit

from app.repositories.visit_audit_repository import (
    VisitAuditRepository,
)

from app.repositories.visit_repository import (
    VisitRepository,
)

from app.common.database import DatabaseSession


class VisitAuditService:

    @staticmethod
    def create(
        visit_id,
        action,
        user_id=None,
        notes=None,
    ):
        visit = VisitRepository.get_by_id(
            visit_id
        )

        if not visit:
            raise NotFoundError(
                "Visit not found."
            )

        audit = VisitAudit(
            visit_id=visit.id,
            user_id=user_id,
            action=action,
            notes=notes,
        )

        audit = VisitAuditRepository.create(
            audit
        )

        DatabaseSession.flush()

        return audit

    @staticmethod
    def get_by_visit_id(visit_id):

        visit = VisitRepository.get_by_id(
            visit_id
        )

        if not visit:
            raise NotFoundError(
                "Visit not found."
            )

        return (
            VisitAuditRepository
            .get_by_visit_id(visit_id)
        )

    @staticmethod
    def get_by_id(audit_id):

        audit = (
            VisitAuditRepository
            .get_by_id(audit_id)
        )

        if not audit:
            raise NotFoundError(
                "Audit record not found."
            )

        return audit