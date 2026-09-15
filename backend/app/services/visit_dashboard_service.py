from datetime import (
    datetime,
    time,
    timedelta,
)
 
from app.common.constants import (
    VisitStatus,
)
 
from app.repositories.visit_repository import (
    VisitRepository,
)
 
 
class VisitDashboardService:
 
    @staticmethod
    def get_summary(filters):
 
        start_date = filters.get(
            "start_date"
        )
 
        end_date = filters.get(
            "end_date"
        )
 
 
        start_datetime = None
 
        if start_date:
            start_datetime = (
                datetime.combine(
                    start_date,
                    time.min,
                )
            )
 
 
        end_datetime = None
 
        if end_date:
            # Exclusive upper boundary.
            #
            # 2026-09-07 becomes:
            # created_at < 2026-09-08 00:00
            end_datetime = (
                datetime.combine(
                    end_date
                    + timedelta(days=1),
                    time.min,
                )
            )
 
 
        summary = (
            VisitRepository
            .dashboard_summary(
                status=filters.get(
                    "status"
                ),
 
                site_id=filters.get(
                    "site_id"
                ),
 
                visit_type=filters.get(
                    "visit_type"
                ),
 
                start_date=
                    start_datetime,
 
                end_date=
                    end_datetime,
            )
        )
 
 
        breakdown = (
            summary[
                "status_breakdown"
            ]
        )
 
 
        return {
            "total_visits":
                summary[
                    "total_visits"
                ],
 
            "pending_approval":
                breakdown.get(
                    VisitStatus.PENDING,
                    0,
                ),
 
            "approved":
                breakdown.get(
                    VisitStatus.APPROVED,
                    0,
                ),
 
            "checked_in":
                breakdown.get(
                    VisitStatus.CHECKED_IN,
                    0,
                ),
 
            "checked_out":
                breakdown.get(
                    VisitStatus.CHECKED_OUT,
                    0,
                ),
 
            "status_breakdown":
                breakdown,
 
            "visit_type_breakdown":
                summary[
                    "visit_type_breakdown"
                ],
        }