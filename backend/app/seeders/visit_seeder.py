from datetime import (
    datetime,
    timedelta,
    timezone,
)
 
from app.common.constants import (
    VisitStatus,
    VisitType,
)
 
from app.models.visit import Visit
 
 
class VisitSeeder:
 
    @staticmethod
    def run(
        visitor,
        host,
        destination,
        site,
    ):
 
        visit = (
            Visit.query
            .filter_by(
                visitor_id=visitor.id,
                host_id=host.id,
                purpose="Seeded business meeting",
            )
            .first()
        )
 
        if visit:
            return visit
 
        now = datetime.now(
            timezone.utc
        ).replace(
            tzinfo=None
        )
 
        visit = Visit(
            visitor_id=visitor.id,
            host_id=host.id,
            destination_id=destination.id,
            site_id=site.id,
 
            visit_type=VisitType.PREBOOKED,
            status=VisitStatus.PENDING,
 
            purpose="Seeded business meeting",
 
            expected_arrival=(
                now
                + timedelta(hours=2)
            ),
 
            expected_departure=(
                now
                + timedelta(hours=4)
            ),
 
            checked_in_at=None,
            checked_out_at=None,
 
            approved_by=None,
            approved_at=None,
 
            badge_number=None,
 
            visitor_code=None,
            visitor_code_generated_at=None,
 
            qr_token=None,
            qr_generated_at=None,
 
            notes="Seeded visit",
        )
 
        return visit