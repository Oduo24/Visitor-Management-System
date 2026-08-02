from flask import Blueprint
from flask import request

from flask_jwt_extended import jwt_required

from app.common.responses import success

from app.authorization.permissions import Permission
from app.common.decorators import permission_required

from app.schemas.prebook_visit_schema import (
    PrebookVisitCreateSchema,
)

from app.schemas.visit_schema import (
    VisitResponseSchema,
)

from app.services.prebook_visit_service import (
    PrebookVisitService,
)


prebook_visit_bp = Blueprint(
    "prebook_visits",
    __name__,
    url_prefix="/api/visits/prebook",
)

create_schema = PrebookVisitCreateSchema()

response_schema = VisitResponseSchema()


@prebook_visit_bp.post("")
@jwt_required()
@permission_required(Permission.VISIT_CREATE)
def create_prebook_visit():

    data = create_schema.load(
        request.get_json()
    )

    visit = PrebookVisitService.create(data)

    return success(
        data=response_schema.dump(visit),
        status_code=201,
    )