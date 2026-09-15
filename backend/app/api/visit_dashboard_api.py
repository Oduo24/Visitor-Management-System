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
 
from app.schemas.visit_dashboard_schema import (
    VisitDashboardQuerySchema,
    VisitDashboardResponseSchema,
)
 
from app.services.visit_dashboard_service import (
    VisitDashboardService,
)
 
 
visit_dashboard_bp = Blueprint(
    "visit_dashboard",
    __name__,
)
 
 
query_schema = (
    VisitDashboardQuerySchema()
)
 
response_schema = (
    VisitDashboardResponseSchema()
)
 
 
@visit_dashboard_bp.get(
    "/dashboard"
)
@jwt_required()
@permission_required(
    Permission.REPORT_VIEW
)
def get_dashboard():
 
    filters = query_schema.load(
        request.args
    )
 
    dashboard = (
        VisitDashboardService
        .get_summary(filters)
    )
 
    return success(
        data=response_schema.dump(
            dashboard
        )
    )