from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission

from app.common.decorators import permission_required
from app.common.responses import success

from app.schemas.visit_schema import VisitResponseSchema

from app.services.visit_checkin_service import (
    VisitCheckinService,
)


checkin_bp = Blueprint(
    "visit_checkin",
    __name__,
    url_prefix="/api/visits",
)


response_schema = VisitResponseSchema()


@checkin_bp.post("/<visit_id>/check-in")
@jwt_required()
@permission_required(
    Permission.VISIT_CHECKIN
)
def check_in_visit(visit_id):

    visit = VisitCheckinService.check_in(
        visit_id
    )

    return success(
        data=response_schema.dump(visit)
    )