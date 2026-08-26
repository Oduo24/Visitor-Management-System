from flask import Blueprint
 
from app.common.responses import success
 
from app.schemas.visit_access_pass_schema import (
    VisitAccessPassResponseSchema,
)
 
from app.services.visit_access_pass_service import (
    VisitAccessPassService,
)
 
 
visit_access_pass_bp = Blueprint(
    "visit_access_pass",
    __name__,
)
 
 
@visit_access_pass_bp.get(
    "/access-pass/<token>"
)
def get_visit_access_pass(
    token,
):
 
    data = (
        VisitAccessPassService
        .get_public_details(
            token
        )
    )
 
    result = (
        VisitAccessPassResponseSchema()
        .dump(
            data
        )
    )
 
    return success(
        data=result
    )