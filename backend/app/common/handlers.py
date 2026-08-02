from flask import jsonify
from marshmallow import ValidationError as MarshmallowValidationError

from app.common.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
)
from app.common.responses import error


def register_error_handlers(app):

    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        return error(str(e), 404)

    @app.errorhandler(ConflictError)
    def handle_conflict(e):
        return error(str(e), 409)

    @app.errorhandler(ValidationError)
    def handle_validation(e):
        return error(str(e), 400)

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow(e):
        return error(
            message="Validation failed.",
            status_code=400,
            errors=e.messages,
        )

    @app.errorhandler(AuthenticationError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "message": str(error),
        }), 401

    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(error):
        return {
            "success": False,
            "message": error.message,
        }, error.status_code

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception(e)
        return error("Internal server error.", 500)



    
    