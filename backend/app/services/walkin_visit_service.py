from app.common.constants import VisitType

from app.services.visit_service import VisitService


class WalkinVisitService:

    @staticmethod
    def create(data):

        data["visit_type"] = VisitType.WALK_IN

        return VisitService.create(data)