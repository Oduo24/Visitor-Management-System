from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission

from app.common.decorators import permission_required
from app.common.responses import success

from app.schemas.visit_schema import VisitResponseSchema

from app.services.badge_service import BadgeService


badge_bp = Blueprint(
    "badges",
    __name__,
    url_prefix="/api/visits",
)


response_schema = VisitResponseSchema()


@badge_bp.post("/<visit_id>/badge")
@jwt_required()
@permission_required(Permission.VISIT_CHECKIN)
def issue_badge(visit_id):

    visit = BadgeService.issue(
        visit_id
    )

    return success(
        data=response_schema.dump(visit),
        status_code=200,
    )