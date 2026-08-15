from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission

from app.common.decorators import permission_required
from app.common.responses import success

from app.schemas.visit_schema import VisitResponseSchema

from app.services.visit_checkout_service import (
    VisitCheckoutService,
)


checkout_bp = Blueprint(
    "visit_checkout",
    __name__,
    url_prefix="/api/visits",
)


response_schema = VisitResponseSchema()


@checkout_bp.post("/<visit_id>/check-out")
@jwt_required()
@permission_required(
    Permission.VISIT_CHECKOUT
)
def check_out_visit(visit_id):

    visit = VisitCheckoutService.check_out(
        visit_id
    )

    return success(
        data=response_schema.dump(visit)
    )