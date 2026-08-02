from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.common.responses import success

from app.schemas.visitor_schema import (
    VisitorCreateSchema,
    VisitorUpdateSchema,
    VisitorResponseSchema,
)

from app.services.visitor_service import VisitorService

from app.common.decorators import permission_required

from app.authorization.permissions import Permission


visitor_bp = Blueprint(
    "visitors",
    __name__,
    url_prefix="/api/visitors",
)

create_schema = VisitorCreateSchema()
update_schema = VisitorUpdateSchema()

response_schema = VisitorResponseSchema()
response_many_schema = VisitorResponseSchema(many=True)


@visitor_bp.get("")
@jwt_required()
@permission_required(Permission.VISITOR_READ)
def get_visitors():

    q = request.args.get("q")

    if q:
        visitors = VisitorService.search(q)
    else:
        visitors = VisitorService.get_all()

    return success(
        data=response_many_schema.dump(visitors)
    )

@visitor_bp.get("/<visitor_id>")
@jwt_required()
@permission_required(Permission.VISITOR_READ)
def get_visitor(visitor_id):

    visitor = VisitorService.get_by_id(
        visitor_id
    )

    return success(
        data=response_schema.dump(visitor)
    )


@visitor_bp.post("")
@jwt_required()
@permission_required(Permission.VISITOR_CREATE)
def create_visitor():

    data = create_schema.load(
        request.get_json()
    )

    visitor = VisitorService.create(data)

    return success(
    message="Visitor created successfully.",
    data=response_schema.dump(visitor),
    status_code=201,
    )

@visitor_bp.put("/<visitor_id>")
@jwt_required()
@permission_required(Permission.VISITOR_UPDATE)
def update_visitor(visitor_id):

    data = update_schema.load(
        request.get_json()
    )

    visitor = VisitorService.update(
        visitor_id,
        data,
    )

    return success(
        data=response_schema.dump(visitor)
    )

@visitor_bp.delete("/<visitor_id>")
@jwt_required()
@permission_required(Permission.VISITOR_DELETE)
def delete_visitor(visitor_id):

    VisitorService.delete(visitor_id)

    return success(
        message="Visitor deleted successfully."
    )