from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.common.responses import success
from app.schemas.role_schema import (
    RoleCreateSchema,
    RoleUpdateSchema,
    RoleResponseSchema,
)
from app.services.role_service import RoleService

from app.authorization.permissions import Permission
from app.common.decorators import permission_required


role_bp = Blueprint("roles", __name__)

create_schema = RoleCreateSchema()
update_schema = RoleUpdateSchema()

response_schema = RoleResponseSchema()
response_many_schema = RoleResponseSchema(many=True)


@role_bp.get("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_roles():
    roles = RoleService.get_all()

    return success(
        data=response_many_schema.dump(roles)
    )


@role_bp.get("/<string:role_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def get_role(role_id):
    role = RoleService.get_by_id(role_id)

    return success(
        data=response_schema.dump(role)
    )


@role_bp.post("")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def create_role():
    data = create_schema.load(request.get_json())

    role = RoleService.create(data)

    return success(
        message="Role created successfully.",
        data=response_schema.dump(role),
        status_code=201,
    )


@role_bp.put("/<string:role_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def update_role(role_id):
    data = update_schema.load(request.get_json())

    role = RoleService.update(
        role_id,
        data,
    )

    return success(
        message="Role updated successfully.",
        data=response_schema.dump(role),
    )


@role_bp.delete("/<string:role_id>")
@jwt_required()
@permission_required(Permission.SETTINGS_MANAGE)
def delete_role(role_id):
    RoleService.delete(role_id)

    return success(
        message="Role deleted successfully."
    )