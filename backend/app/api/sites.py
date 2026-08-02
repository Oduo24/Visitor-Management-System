from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.common.responses import success
from app.schemas.site_schema import (
    SiteCreateSchema,
    SiteUpdateSchema,
    SiteResponseSchema,
)
from app.services.site_service import SiteService

from app.authorization.permissions import Permission
from app.common.decorators import permission_required

site_bp = Blueprint("sites", __name__)

create_schema = SiteCreateSchema()
update_schema = SiteUpdateSchema()

response_schema = SiteResponseSchema()
response_many_schema = SiteResponseSchema(many=True)


@site_bp.get("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_sites():
    return success(
        data=response_many_schema.dump(
            SiteService.get_all()
        )
    )


@site_bp.get("/<string:site_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_site(site_id):
    return success(
        data=response_schema.dump(
            SiteService.get_by_id(site_id)
        )
    )


@site_bp.post("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def create_site():
    data = create_schema.load(request.get_json())

    site = SiteService.create(data)

    return success(
        message="Site created successfully.",
        data=response_schema.dump(site),
        status_code=201,
    )


@site_bp.put("/<string:site_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def update_site(site_id):
    data = update_schema.load(request.get_json())

    site = SiteService.update(site_id, data)

    return success(
        message="Site updated successfully.",
        data=response_schema.dump(site),
    )


@site_bp.delete("/<string:site_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def delete_site(site_id):
    SiteService.delete(site_id)

    return success(
        message="Site deleted successfully."
    )