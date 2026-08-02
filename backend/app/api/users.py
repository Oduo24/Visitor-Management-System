from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.common.responses import success

from app.schemas.user_schema import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
)

from app.services.user_service import UserService

from app.authorization.permissions import Permission
from app.common.decorators import permission_required


user_bp = Blueprint("users", __name__)

create_schema = UserCreateSchema()
update_schema = UserUpdateSchema()

response_schema = UserResponseSchema()
response_many_schema = UserResponseSchema(many=True)


@user_bp.get("")
@jwt_required()
@permission_required(Permission.USER_READ)
def get_users():
    users = UserService.get_all()

    return success(
        data=response_many_schema.dump(users)
    )


@user_bp.get("/<string:user_id>")
@jwt_required()
@permission_required(Permission.USER_READ)
def get_user(user_id):
    user = UserService.get_by_id(user_id)

    return success(
        data=response_schema.dump(user)
    )


@user_bp.post("")
@jwt_required()
@permission_required(Permission.USER_CREATE)
def create_user():
    data = create_schema.load(request.get_json())

    user = UserService.create(data)

    return success(
        message="User created successfully.",
        data=response_schema.dump(user),
        status_code=201,
    )


@user_bp.put("/<string:user_id>")
@jwt_required()
@permission_required(Permission.USER_UPDATE)
def update_user(user_id):
    data = update_schema.load(request.get_json())

    user = UserService.update(
        user_id,
        data,
    )

    return success(
        message="User updated successfully.",
        data=response_schema.dump(user),
    )


@user_bp.delete("/<string:user_id>")
@jwt_required()
@permission_required(Permission.USER_DELETE)
def delete_user(user_id):
    UserService.delete(user_id)

    return success(
        message="User deleted successfully."
    )