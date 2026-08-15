import re

from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError

from app.common.constants import VisitStatus

from app.services.visit_service import VisitService


class BadgeService:

    @staticmethod
    def issue(visit_id):

        visit = VisitService.get_by_id(
            visit_id
        )

        if visit.status != VisitStatus.APPROVED:
            raise ConflictError(
                "Badge can only be issued for an approved visit."
            )

        if visit.badge_number:
            raise ConflictError(
                "Badge has already been issued."
            )

        badge_number = BadgeService._generate_badge_number()

        visit.badge_number = badge_number

        DatabaseSession.commit()

        return visit

    @staticmethod
    def _generate_badge_number():

        from app.models.visit import Visit

        visits = (
            Visit.query
            .filter(
                Visit.badge_number.isnot(None)
            )
            .all()
        )

        highest_number = 0

        for visit in visits:

            match = re.fullmatch(
                r"B(\d+)",
                visit.badge_number,
            )

            if not match:
                continue

            number = int(
                match.group(1)
            )

            highest_number = max(
                highest_number,
                number,
            )

        return f"B{highest_number + 1:03d}"