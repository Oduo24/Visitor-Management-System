"""
Custom application exceptions.

These exceptions represent business-level errors and are translated
into HTTP responses by the global error handlers.
"""


class AppException(Exception):
    """Base class for all application-specific exceptions."""

    default_message = "An application error occurred."

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)


class NotFoundError(AppException):
    """Raised when a requested resource cannot be found."""

    default_message = "Resource not found."


class ValidationError(AppException):
    """Raised when business validation fails."""

    default_message = "Validation failed."


class ConflictError(AppException):
    """Raised when a resource already exists."""

    default_message = "Resource already exists."


class UnauthorizedError(AppException):
    """Raised when authentication is required."""

    default_message = "Authentication required."


class ForbiddenError(AppException):
    """Raised when the user lacks permission."""

    default_message = "You do not have permission to perform this action."

class AuthenticationError(Exception):
    pass

class AuthorizationError(Exception):

    status_code = 403

    def __init__(self, message):
        self.message = message