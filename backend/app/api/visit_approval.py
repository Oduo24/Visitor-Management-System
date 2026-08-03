from flask import Blueprint, request

from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission

from app.common.decorators import permission_required
from app.common.responses import success

from app.schemas.visit_schema import VisitResponseSchema
from app.schemas.visit_approval_schema import VisitApprovalSchema

from app.services.visit_approval_service import (
    VisitApprovalService,
)

approval_bp = Blueprint(
    "visit_approval",
    __name__,
    url_prefix="/api/visits",
)

schema = VisitApprovalSchema()

response_schema = VisitResponseSchema()


@approval_bp.patch("/<visit_id>/approval")
@jwt_required()
@permission_required(Permission.VISIT_APPROVE)
def approve_visit(visit_id):

    data = schema.load(
        request.get_json()
    )

    visit = VisitApprovalService.approve(
        visit_id,
        approved=data["approved"],
        notes=data.get("notes"),
    )

    return success(
        data=response_schema.dump(visit)
    )