from datetime import datetime

from flask import Blueprint, request

from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission

from app.common.decorators import permission_required
from app.common.responses import success

from app.schemas.visit_schema import VisitResponseSchema

from app.services.visit_service import VisitService


visit_dashboard_bp = Blueprint(
    "visit_dashboard",
    __name__,
    url_prefix="/api/visits",
)

response_schema = VisitResponseSchema(
    many=True
)


@visit_dashboard_bp.get("/dashboard")
@jwt_required()
@permission_required(
    Permission.VISIT_READ
)
def visit_dashboard():

    status = request.args.get(
        "status"
    )

    site_id = request.args.get(
        "site_id"
    )

    visit_type = request.args.get(
        "visit_type"
    )

    start_date = request.args.get(
        "start_date"
    )

    end_date = request.args.get(
        "end_date"
    )

    parsed_start_date = None
    parsed_end_date = None

    if start_date:
        parsed_start_date = datetime.fromisoformat(
            start_date
        )

    if end_date:
        parsed_end_date = datetime.fromisoformat(
            end_date
        )

    visits = VisitService.dashboard(
        status=status,
        site_id=site_id,
        visit_type=visit_type,
        start_date=parsed_start_date,
        end_date=parsed_end_date,
    )

    return success(
        data=response_schema.dump(
            visits
        )
    )