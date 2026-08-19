
from app.extensions import db
from app.models.visit_invitation import VisitInvitation


class VisitInvitationRepository:

    @staticmethod
    def create(invitation):
        db.session.add(invitation)
        return invitation

    @staticmethod
    def get_by_id(invitation_id):
        return db.session.get(
            VisitInvitation,
            invitation_id,
        )

    @staticmethod
    def get_by_token(token):
        return (
            VisitInvitation.query
            .filter(
                VisitInvitation.token == token
            )
            .first()
        )

    @staticmethod
    def get_by_visit_id(visit_id):
        return (
            VisitInvitation.query
            .filter(
                VisitInvitation.visit_id == visit_id
            )
            .order_by(
                VisitInvitation.created_at.desc()
            )
            .all()
        )