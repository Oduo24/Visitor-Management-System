import secrets
from datetime import datetime, timedelta, timezone

from app.common.database import DatabaseSession
from app.common.exceptions import (
    ConflictError,
    NotFoundError,
)

from app.models.visit_invitation import VisitInvitation
from app.repositories.visit_invitation_repository import (
    VisitInvitationRepository,
)
from app.services.visit_service import VisitService


class VisitInvitationService:

    DEFAULT_EXPIRY_HOURS = 48

    @staticmethod
    def _utc_now():
        """
        Return the current UTC time as a naive datetime.

        The application currently persists DateTime values
        without timezone information, so we normalize UTC
        to a naive datetime at the database boundary.
        """
        return datetime.now(
            timezone.utc
        ).replace(
            tzinfo=None
        )

    @staticmethod
    def create(
        visit_id,
        expiry_hours=None,
    ):

        visit = VisitService.get_by_id(
            visit_id
        )

        existing = (
            VisitInvitationRepository
            .get_by_visit_id(
                visit.id
            )
        )

        now = (
            VisitInvitationService
            ._utc_now()
        )

        for invitation in existing:

            if (
                invitation.completed_at is None
                and invitation.expires_at > now
            ):
                raise ConflictError(
                    "An active invitation already exists."
                )

        if expiry_hours is None:
            expiry_hours = (
                VisitInvitationService
                .DEFAULT_EXPIRY_HOURS
            )

        if expiry_hours <= 0:
            raise ConflictError(
                "Invitation expiry must be greater than zero."
            )

        invitation = VisitInvitation(
            visit_id=visit.id,
            token=secrets.token_urlsafe(32),
            expires_at=(
                now
                + timedelta(
                    hours=expiry_hours
                )
            ),
        )

        VisitInvitationRepository.create(
            invitation
        )

        DatabaseSession.commit()

        return invitation

    @staticmethod
    def get_by_token(token):

        invitation = (
            VisitInvitationRepository
            .get_by_token(token)
        )

        if not invitation:
            raise NotFoundError(
                "Invitation not found."
            )

        now = (
            VisitInvitationService
            ._utc_now()
        )

        if invitation.completed_at:
            raise ConflictError(
                "Invitation has already been completed."
            )

        if invitation.expires_at <= now:
            raise ConflictError(
                "Invitation has expired."
            )

        return invitation

    @staticmethod
    def get_public_details(token):

        invitation = (
            VisitInvitationService
            .get_by_token(token)
        )

        visit = invitation.visit
        visitor = visit.visitor

        return {
            "visit_id": visit.id,
            "site": visit.site.name,
            "host": (
                f"{visit.host.first_name} "
                f"{visit.host.last_name}"
            ),
            "visit_type": visit.visit_type,
            "expected_arrival": (
                visit.expected_arrival
            ),
            "purpose": visit.purpose,
            "visitor": {
                "first_name": visitor.first_name,
                "middle_name": (
                    visitor.middle_name
                ),
                "last_name": visitor.last_name,
                "phone": visitor.phone,
                "email": visitor.email,
                "id_number": visitor.id_number,
                "passport_number": (
                    visitor.passport_number
                ),
                "vehicle_registration": (
                    visitor.vehicle_registration
                ),
            },
            "expires_at": invitation.expires_at,
        }

    @staticmethod
    def complete(
        token,
        data,
    ):

        invitation = (
            VisitInvitationService
            .get_by_token(token)
        )

        visitor = invitation.visit.visitor

        allowed_fields = {
            "first_name",
            "middle_name",
            "last_name",
            "phone",
            "email",
            "id_number",
            "passport_number",
            "vehicle_registration",
        }

        for field, value in data.items():

            if field in allowed_fields:
                setattr(
                    visitor,
                    field,
                    value,
                )

        invitation.completed_at = (
            VisitInvitationService
            ._utc_now()
        )

        DatabaseSession.commit()

        return invitation