from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.common.responses import success

from app.schemas.visit_schema import (
    VisitCreateSchema,
    VisitUpdateSchema,
    VisitResponseSchema,
)

from app.services.visit_service import VisitService

from app.authorization.permissions import Permission
from app.common.decorators import permission_required


visit_bp = Blueprint(
    "visits",
    __name__,
    url_prefix="/api/visits",
)

create_schema = VisitCreateSchema()
update_schema = VisitUpdateSchema()

response_schema = VisitResponseSchema()
response_many_schema = VisitResponseSchema(many=True)


@visit_bp.get("")
@jwt_required()
@permission_required(Permission.VISIT_READ)
def get_visits():

    q = request.args.get("q")

    # if q:
    #     visits = VisitService.search(q)  --VisitService.search not implemented yet

    visits = VisitService.get_all()

    return success(
        data=response_many_schema.dump(visits)
    )


@visit_bp.get("/<string:visit_id>")
@jwt_required()
@permission_required(Permission.VISIT_READ)
def get_visit(visit_id):

    visit = VisitService.get_by_id(
        visit_id
    )

    return success(
        data=response_schema.dump(visit)
    )


@visit_bp.post("")
@jwt_required()
@permission_required(Permission.VISIT_CREATE)
def create_visit():

    data = create_schema.load(
        request.get_json()
    )

    visit = VisitService.create(data)

    return success(
        message="Visit created successfully.",
        data=response_schema.dump(visit),
        status_code=201,
    )


# @visit_bp.put("/<string:visit_id>")
# @jwt_required()
# @permission_required(Permission.VISIT_UPDATE)
# def update_visit(visit_id):

#     data = update_schema.load(
#         request.get_json()
#     )

#     visit = VisitService.update(  ---VisitService.update not implemented yet
#         visit_id,
#         data,
#     )

#     return success(
#         message="Visit updated successfully.",
#         data=response_schema.dump(visit),
#     )


@visit_bp.delete("/<string:visit_id>")
@jwt_required()
@permission_required(Permission.VISIT_DELETE)
def delete_visit(visit_id):

    VisitService.delete(
        visit_id
    )

    return success(
        message="Visit deleted successfully."
    )