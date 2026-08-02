from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.common.responses import success
from app.schemas.destination_schema import (
    DestinationCreateSchema,
    DestinationUpdateSchema,
    DestinationResponseSchema,
)
from app.services.destination_service import DestinationService

from app.authorization.permissions import Permission
from app.common.decorators import permission_required

destination_bp = Blueprint("destinations", __name__)

create_schema = DestinationCreateSchema()
update_schema = DestinationUpdateSchema()

response_schema = DestinationResponseSchema()
response_many_schema = DestinationResponseSchema(many=True)


@destination_bp.get("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_destinations():
    destinations = DestinationService.get_all()

    return success(
        data=response_many_schema.dump(destinations)
    )


@destination_bp.get("/<string:destination_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_destination(destination_id):
    destination = DestinationService.get_by_id(destination_id)

    return success(
        data=response_schema.dump(destination)
    )


@destination_bp.post("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def create_destination():
    data = create_schema.load(request.get_json())

    destination = DestinationService.create(data)

    return success(
        message="Destination created successfully.",
        data=response_schema.dump(destination),
        status_code=201,
    )


@destination_bp.put("/<string:destination_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def update_destination(destination_id):
    data = update_schema.load(request.get_json())

    destination = DestinationService.update(
        destination_id,
        data,
    )

    return success(
        message="Destination updated successfully.",
        data=response_schema.dump(destination),
    )


@destination_bp.delete("/<string:destination_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def delete_destination(destination_id):
    DestinationService.delete(destination_id)

    return success(
        message="Destination deleted successfully."
    )