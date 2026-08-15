from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission

from app.common.decorators import permission_required
from app.common.responses import success

from app.schemas.visit_schema import VisitResponseSchema

from app.services.visit_qr_service import VisitQRService


qr_bp = Blueprint(
    "visit_qr",
    __name__,
    url_prefix="/api/visits",
)


response_schema = VisitResponseSchema()


@qr_bp.post("/<visit_id>/qr")
@jwt_required()
@permission_required(
    Permission.VISIT_READ
)
def generate_visit_qr(visit_id):

    visit = VisitQRService.generate(
        visit_id
    )

    return success(
        data=response_schema.dump(visit)
    )