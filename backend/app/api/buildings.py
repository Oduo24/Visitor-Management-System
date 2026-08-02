from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.common.responses import success
from app.schemas.building_schema import (
    BuildingCreateSchema,
    BuildingUpdateSchema,
    BuildingResponseSchema,
)
from app.services.building_service import BuildingService

from app.authorization.permissions import Permission
from app.common.decorators import permission_required

building_bp = Blueprint("buildings", __name__)

create_schema = BuildingCreateSchema()
update_schema = BuildingUpdateSchema()

response_schema = BuildingResponseSchema()
response_many_schema = BuildingResponseSchema(many=True)


@building_bp.get("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_buildings():
    """Return all buildings."""

    buildings = BuildingService.get_all()

    return success(
        data=response_many_schema.dump(buildings)
    )


@building_bp.get("/<string:building_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_building(building_id):
    """Return a single building."""

    building = BuildingService.get_by_id(building_id)

    return success(
        data=response_schema.dump(building)
    )


@building_bp.post("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def create_building():
    """Create a building."""

    data = create_schema.load(request.get_json())

    building = BuildingService.create(data)

    return success(
        message="Building created successfully.",
        data=response_schema.dump(building),
        status_code=201,
    )


@building_bp.put("/<string:building_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def update_building(building_id):
    """Update a building."""

    data = update_schema.load(request.get_json())

    building = BuildingService.update(
        building_id,
        data,
    )

    return success(
        message="Building updated successfully.",
        data=response_schema.dump(building),
    )


@building_bp.delete("/<string:building_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def delete_building(building_id):
    """Delete a building."""

    BuildingService.delete(building_id)

    return success(
        message="Building deleted successfully."
    )