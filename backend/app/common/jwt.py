from flask_jwt_extended import JWTManager

from app.repositories.user_repository import UserRepository


def register_jwt_callbacks(jwt: JWTManager):

    @jwt.user_lookup_loader
    def load_user(jwt_header, jwt_data):

        identity = jwt_data["sub"]

        return UserRepository.get_by_id(
            identity
        )

