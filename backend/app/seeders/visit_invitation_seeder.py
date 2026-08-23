from datetime import (
    datetime,
    timedelta,
    timezone,
)
 
from app.models.visit_invitation import (
    VisitInvitation,
)
 
 
class VisitInvitationSeeder:
 
    @staticmethod
    def run(visit):
 
        invitation = (
            VisitInvitation.query
            .filter_by(
                visit_id=visit.id,
            )
            .first()
        )
 
        if invitation:
            return invitation
 
        now = datetime.now(
            timezone.utc
        ).replace(
            tzinfo=None
        )
 
        invitation = VisitInvitation(
            visit_id=visit.id,
            token=(
                "seed-visitor-invitation-"
                "token"
            ),
            expires_at=(
                now
                + timedelta(days=7)
            ),
            completed_at=None,
        )
 
        return invitation