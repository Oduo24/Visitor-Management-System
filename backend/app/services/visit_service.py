from app.common.database import DatabaseSession

from app.common.exceptions import NotFoundError

from app.models.visit import Visit

from app.common.constants import (
    VisitStatus,
    VisitAuditAction,
)

from app.services.visit_audit_service import (
    VisitAuditService,
)

from app.repositories.visit_repository import VisitRepository
from app.repositories.visitor_repository import VisitorRepository
from app.repositories.user_repository import UserRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.destination_repository import DestinationRepository


class VisitService:

    @staticmethod
    def get_all():
        return VisitRepository.get_all()

    @staticmethod
    def get_by_id(visit_id):

        visit = VisitRepository.get_by_id(
            visit_id
        )

        if not visit:
            raise NotFoundError(
                "Visit not found."
            )

        return visit

    @staticmethod
    def create(data):

        visitor = VisitorRepository.get_by_id(
            data["visitor_id"]
        )

        if not visitor:
            raise NotFoundError(
                "Visitor not found."
            )

        host = UserRepository.get_by_id(
            data["host_id"]
        )

        if not host:
            raise NotFoundError(
                "Host not found."
            )

        site = SiteRepository.get_by_id(
            data["site_id"]
        )

        if not site:
            raise NotFoundError(
                "Site not found."
            )

        destination = DestinationRepository.get_by_id(
            data["destination_id"]
        )

        if not destination:
            raise NotFoundError(
                "Destination not found."
            )

        visit = Visit(
            visitor_id=data["visitor_id"],
            host_id=data["host_id"],
            destination_id=data["destination_id"],
            site_id=data["site_id"],
            visit_type=data["visit_type"],
            status=VisitStatus.PENDING,
            purpose=data.get("purpose"),
            expected_arrival=data.get("expected_arrival"),
            expected_departure=data.get("expected_departure"),
            notes=data.get("notes"),
        )

        VisitRepository.create(visit)
        
        DatabaseSession.flush()

        VisitAuditService.create(
            visit_id=visit.id,
            action=VisitAuditAction.CREATED,
        )

        DatabaseSession.commit()

        return visit

    @staticmethod
    def delete(visit_id):

        visit = VisitRepository.get_by_id(
            visit_id
        )

        if not visit:
            raise NotFoundError(
                "Visit not found."
            )

        VisitRepository.delete(
            visit
        )

        DatabaseSession.commit()

    @staticmethod
    def search(query):
        return VisitRepository.search(query)

    @staticmethod
    def dashboard(
        status=None,
        site_id=None,
        visit_type=None,
        start_date=None,
        end_date=None,
    ):
        return VisitRepository.dashboard(
            status=status,
            site_id=site_id,
            visit_type=visit_type,
            start_date=start_date,
            end_date=end_date,
        )