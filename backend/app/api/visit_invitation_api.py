# app/api/visit_invitation_api.py

from flask import Blueprint

from flask_jwt_extended import jwt_required

from app.authorization.permissions import Permission
from app.common.decorators import permission_required
from app.common.responses import success

from app.services.visit_invitation_service import (
    VisitInvitationService,
)


invitation_bp = Blueprint(
    "visit_invitation",
    __name__,
    url_prefix="/api/visits",
)


@invitation_bp.post(
    "/<visit_id>/invitation"
)
@jwt_required()
@permission_required(
    Permission.VISIT_CREATE
)
def create_visit_invitation(
    visit_id,
):

    invitation = (
        VisitInvitationService.create(
            visit_id
        )
    )

    return success(
        data={
            "id": str(invitation.id),
            "visit_id": str(
                invitation.visit_id
            ),
            "token": invitation.token,
            "expires_at": (
                invitation.expires_at.isoformat()
            ),
        }
    )


@invitation_bp.get(
    "/invitations/<token>"
)
def get_visit_invitation(token):

    invitation = (
        VisitInvitationService
        .get_by_token(token)
    )

    visit = invitation.visit

    return success(
        data={
            "visit_id": str(
                visit.id
            ),
            "expires_at": (
                invitation.expires_at.isoformat()
            ),
        }
    )