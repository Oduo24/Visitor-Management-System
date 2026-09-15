from flask import (
    Blueprint,
    request,
)
 
from flask_jwt_extended import (
    jwt_required,
)
 
from app.authorization.permissions import (
    Permission,
)
 
from app.common.decorators import (
    permission_required,
)
 
from app.common.responses import success
 
from app.schemas.visit_report_schema import (
    VisitActivityReportQuerySchema,
)
 
from app.schemas.visit_schema import (
    VisitResponseSchema,
)
 
from app.services.visit_report_service import (
    VisitReportService,
)
 
 
visit_report_bp = Blueprint(
    "visit_report",
    __name__,
)
 
 
query_schema = (
    VisitActivityReportQuerySchema()
)
 
response_schema = (
    VisitResponseSchema(
        many=True
    )
)
 
 
@visit_report_bp.get(
    "/reports/activity"
)
@jwt_required()
@permission_required(
    Permission.REPORT_VIEW
)
def activity_report():
 
    filters = query_schema.load(
        request.args
    )
 
    visits = (
        VisitReportService
        .get_activity(filters)
    )
 
    return success(
        data=response_schema.dump(
            visits
        )
    )