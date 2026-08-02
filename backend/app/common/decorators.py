from functools import wraps
from flask import request

from flask_jwt_extended import current_user

from app.common.exceptions import AuthorizationError
from app.services.authorization_service import AuthorizationService


def permission_required(permission):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            if not AuthorizationService.has_permission(
                current_user,
                permission,
            ):
                raise AuthorizationError(
                    "You do not have permission to perform this action."
                )

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def site_permission_required(permission):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            site_id = (
                kwargs.get("site_id")
                or request.args.get("site_id")
                or request.json.get("site_id")
            )

            if not AuthorizationService.has_site_permission(
                current_user,
                site_id,
                permission,
            ):
                raise AuthorizationError(
                    "You do not have access to this site."
                )

            return fn(*args, **kwargs)

        return wrapper

    return decorator