from flask import Blueprint, request

from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission

from app.common.decorators import permission_required
from app.common.responses import success

from app.schemas.walkin_visit_schema import (
    WalkinVisitCreateSchema,
)

from app.schemas.visit_schema import (
    VisitResponseSchema,
)

from app.services.walkin_visit_service import (
    WalkinVisitService,
)


walkin_visit_bp = Blueprint(
    "walkin_visits",
    __name__,
    url_prefix="/api/walkin-visits",
)

create_schema = WalkinVisitCreateSchema()

response_schema = VisitResponseSchema()


@walkin_visit_bp.post("")
@jwt_required()
@permission_required(Permission.VISIT_CREATE)
def create_walkin_visit():

    data = create_schema.load(
        request.get_json()
    )

    visit = WalkinVisitService.create(data)

    return success(
        data=response_schema.dump(visit),
        status_code=201,
    )