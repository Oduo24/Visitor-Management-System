from app.common.constants import (
    VisitAuditAction,
)
 
from app.models.visit_audit import (
    VisitAudit,
)
 
 
class VisitAuditSeeder:
 
    @staticmethod
    def run(
        visit,
        user=None,
    ):
 
        audit = (
            VisitAudit.query
            .filter_by(
                visit_id=visit.id,
                action=(
                    VisitAuditAction.CREATED
                ),
            )
            .first()
        )
 
        if audit:
            return audit
 
        audit = VisitAudit(
            visit_id=visit.id,
            user_id=(
                user.id
                if user
                else None
            ),
            action=(
                VisitAuditAction.CREATED
            ),
            notes="Visit created by database seeder.",
        )
 
        return audit