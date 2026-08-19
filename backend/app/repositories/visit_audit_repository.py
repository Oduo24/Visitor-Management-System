from app.extensions import db
from app.models.visit_audit import VisitAudit


class VisitAuditRepository:

    @staticmethod
    def create(audit):
        db.session.add(audit)
        return audit

    @staticmethod
    def get_by_visit_id(visit_id):
        return (
            VisitAudit.query
            .filter(
                VisitAudit.visit_id == visit_id
            )
            .order_by(
                VisitAudit.created_at.asc()
            )
            .all()
        )

    @staticmethod
    def get_by_id(audit_id):
        return db.session.get(
            VisitAudit,
            audit_id,
        )