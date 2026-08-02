from app.services.visit_service import VisitService

from app.common.constants import (
    VisitType,
)


class PrebookVisitService:

    @staticmethod
    def create(data):

        payload = data.copy()

        payload["visit_type"] = VisitType.PREBOOKED

        return VisitService.create(payload)