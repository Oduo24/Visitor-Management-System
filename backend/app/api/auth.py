from flask import Blueprint, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_current_user,
)

from app.common.responses import success

from app.schemas.auth_schema import (
    LoginSchema,
    ChangePasswordSchema,
)

from app.schemas.user_schema import (
    UserResponseSchema,
)

from app.services.auth_service import AuthService


auth_bp = Blueprint(
    "auth",
    __name__,
)

login_schema = LoginSchema()

change_password_schema = ChangePasswordSchema()

user_schema = UserResponseSchema()


@auth_bp.post("/login")
def login():

    data = login_schema.load(
        request.get_json()
    )

    result = AuthService.login(
        data["email"],
        data["password"],
    )

    return success(
        message="Login successful.",
        data={
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "user": user_schema.dump(
                result["user"]
            ),
        },
    )


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    access_token = AuthService.refresh(
        user_id
    )

    return success(
        data={
            "access_token": access_token,
        }
    )


@auth_bp.get("/me")
@jwt_required()
def me():

    user = get_current_user()

    return success(
        data=user_schema.dump(user)
    )


@auth_bp.post("/change-password")
@jwt_required()
def change_password():

    data = change_password_schema.load(
        request.get_json()
    )

    user = get_current_user()

    AuthService.change_password(
        user.id,
        data["old_password"],
        data["new_password"],
    )

    return success(
        message="Password changed successfully."
    )