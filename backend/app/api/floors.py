from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.common.responses import success
from app.schemas.floor_schema import (
    FloorCreateSchema,
    FloorUpdateSchema,
    FloorResponseSchema,
)
from app.services.floor_service import FloorService

from app.authorization.permissions import Permission
from app.common.decorators import permission_required


floor_bp = Blueprint("floors", __name__)

create_schema = FloorCreateSchema()
update_schema = FloorUpdateSchema()

response_schema = FloorResponseSchema()
response_many_schema = FloorResponseSchema(many=True)


@floor_bp.get("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_floors():
    floors = FloorService.get_all()

    return success(
        data=response_many_schema.dump(floors)
    )


@floor_bp.get("/<string:floor_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_floor(floor_id):
    floor = FloorService.get_by_id(floor_id)

    return success(
        data=response_schema.dump(floor)
    )


@floor_bp.post("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def create_floor():
    data = create_schema.load(request.get_json())

    floor = FloorService.create(data)

    return success(
        message="Floor created successfully.",
        data=response_schema.dump(floor),
        status_code=201,
    )


@floor_bp.put("/<string:floor_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def update_floor(floor_id):
    data = update_schema.load(request.get_json())

    floor = FloorService.update(
        floor_id,
        data,
    )

    return success(
        message="Floor updated successfully.",
        data=response_schema.dump(floor),
    )


@floor_bp.delete("/<string:floor_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def delete_floor(floor_id):
    FloorService.delete(floor_id)

    return success(
        message="Floor deleted successfully."
    )