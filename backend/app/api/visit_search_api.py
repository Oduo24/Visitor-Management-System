from flask import Blueprint, request

from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission

from app.common.decorators import permission_required
from app.common.responses import success

from app.schemas.visit_schema import VisitResponseSchema

from app.services.visit_service import VisitService


visit_search_bp = Blueprint(
    "visit_search",
    __name__,
    url_prefix="/api/visits",
)

response_schema = VisitResponseSchema(
    many=True
)


@visit_search_bp.get("/search")
@jwt_required()
@permission_required(
    Permission.VISIT_READ
)
def search_visits():

    query = request.args.get(
        "q",
        "",
    )

    visits = VisitService.search(
        query
    )

    return success(
        data=response_schema.dump(
            visits
        )
    )