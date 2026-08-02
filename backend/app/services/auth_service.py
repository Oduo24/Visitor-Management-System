from datetime import datetime, timezone

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app.common.database import DatabaseSession
from app.common.exceptions import (
    AuthenticationError,
    NotFoundError,
)

from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def login(email, password):

        user = UserRepository.get_by_email(email)

        if not user:
            raise AuthenticationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise AuthenticationError(
                "Account is disabled."
            )

        if not check_password_hash(
            user.password_hash,
            password,
        ):
            raise AuthenticationError(
                "Invalid email or password."
            )

        user.last_login_at = datetime.now(
            timezone.utc
        )

        DatabaseSession.commit()

        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "organization_id": user.organization_id,
            },
        )

        refresh_token = create_refresh_token(
            identity=user.id
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
        }

    @staticmethod
    def refresh(user_id):

        user = UserRepository.get_by_id(user_id)

        if not user:
            raise NotFoundError(
                "User not found."
            )

        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "organization_id": user.organization_id,
            },
        )

        return access_token

    @staticmethod
    def get_current_user(user_id):

        user = UserRepository.get_by_id(user_id)

        if not user:
            raise NotFoundError(
                "User not found."
            )

        return user

    @staticmethod
    def change_password(
        user_id,
        old_password,
        new_password,
    ):

        user = UserRepository.get_by_id(user_id)

        if not user:
            raise NotFoundError(
                "User not found."
            )

        if not check_password_hash(
            user.password_hash,
            old_password,
        ):
            raise AuthenticationError(
                "Current password is incorrect."
            )

        user.password_hash = generate_password_hash(
            new_password
        )

        DatabaseSession.commit()

        return user