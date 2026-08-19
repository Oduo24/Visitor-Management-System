from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission
from app.common.decorators import permission_required
from app.common.responses import success

from app.schemas.visit_audit_schema import (
    VisitAuditResponseSchema,
)

from app.services.visit_audit_service import (
    VisitAuditService,
)


audit_bp = Blueprint(
    "visit_audit",
    __name__,
    url_prefix="/api/visits",
)


response_schema = VisitAuditResponseSchema(
    many=True
)


@audit_bp.get("/<visit_id>/audit")
@jwt_required()
@permission_required(
    Permission.VISIT_READ
)
def get_visit_audit(visit_id):

    audits = (
        VisitAuditService
        .get_by_visit_id(visit_id)
    )

    return success(
        data=response_schema.dump(
            audits
        )
    )