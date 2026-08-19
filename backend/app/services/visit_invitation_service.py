
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
    def create(
        visit_id,
        expiry_hours=None,
    ):
        visit = VisitService.get_by_id(
            visit_id
        )

        existing = (
            VisitInvitationRepository
            .get_by_visit_id(visit.id)
        )

        for invitation in existing:
            if (
                invitation.used_at is None
                and invitation.expires_at
                > datetime.now(timezone.utc).replace(tzinfo=None)
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
            datetime.now(
                timezone.utc
            ).replace(
                tzinfo=None
            )
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

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        if invitation.used_at:
            raise ConflictError(
                "Invitation has already been used."
            )

        if invitation.expires_at <= now:
            raise ConflictError(
                "Invitation has expired."
            )

        return invitation

    @staticmethod
    def use(token):

        invitation = (
            VisitInvitationService
            .get_by_token(token)
        )

        invitation.used_at = (
        datetime.now(
            timezone.utc
        ).replace(
            tzinfo=None
        )
    )

        DatabaseSession.commit()

        return invitation