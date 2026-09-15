from datetime import (
    datetime,
    time,
    timedelta,
)
 
from app.repositories.visit_repository import (
    VisitRepository,
)
 
 
class VisitReportService:
 
    @staticmethod
    def get_activity(filters):
 
        start_date = filters.get(
            "start_date"
        )
 
        end_date = filters.get(
            "end_date"
        )
 
 
        start_datetime = None
 
        if start_date:
            start_datetime = datetime.combine(
                start_date,
                time.min,
            )
 
 
        end_datetime = None
 
        if end_date:
            end_datetime = datetime.combine(
                end_date
                + timedelta(days=1),
                time.min,
            )
 
 
        return VisitRepository.dashboard(
            status=filters.get(
                "status"
            ),
            site_id=filters.get(
                "site_id"
            ),
            visit_type=filters.get(
                "visit_type"
            ),
            start_date=start_datetime,
            end_date=end_datetime,
        )

        