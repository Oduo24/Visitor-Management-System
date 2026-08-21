import secrets
 
from datetime import (
    datetime,
    timezone,
)
 
from app.common.database import (
    DatabaseSession,
)
from app.common.exceptions import (
    ConflictError,
    NotFoundError,
)
 
from app.repositories.visit_repository import (
    VisitRepository,
)
 
 
class VisitCodeService:
 
    MAX_GENERATION_ATTEMPTS = 20
 
    @staticmethod
    def _utc_now():
 
        return datetime.now(
            timezone.utc
        ).replace(
            tzinfo=None
        )
 
    @staticmethod
    def _generate_code():
 
        return str(
            secrets.randbelow(
                900000
            )
            + 100000
        )
 
    @staticmethod
    def ensure_code(
        visit_id,
    ):
 
        visit = (
            VisitRepository.get_by_id(
                visit_id
            )
        )
 
        if not visit:
            raise NotFoundError(
                "Visit not found."
            )
 
        if visit.visitor_code:
            return visit.visitor_code
 
        for _ in range(
            VisitCodeService
            .MAX_GENERATION_ATTEMPTS
        ):
 
            code = (
                VisitCodeService
                ._generate_code()
            )
 
            existing = (
                VisitRepository
                .get_by_visitor_code(
                    code
                )
            )
 
            if not existing:
 
                visit.visitor_code = code
 
                visit.visitor_code_generated_at = (
                    VisitCodeService
                    ._utc_now()
                )
 
                DatabaseSession.commit()
 
                return code
 
        raise ConflictError(
            "Unable to generate a unique "
            "visitor code."
        )
 
    @staticmethod
    def get_by_code(
        code,
    ):
 
        if not code:
            raise NotFoundError(
                "Invalid visitor code."
            )
 
        visit = (
            VisitRepository
            .get_by_visitor_code(
                code
            )
        )
 
        if not visit:
            raise NotFoundError(
                "Invalid visitor code."
            )
 
        return visit