from sqlalchemy import or_

from app.extensions import db
from app.models.visit import Visit
from app.models.visitor import Visitor


class VisitRepository:

    @staticmethod
    def create(visit):
        db.session.add(visit)
        return visit

    @staticmethod
    def get_all():
        return (
            Visit.query
            .order_by(Visit.created_at.desc())
            .all()
        )

    @staticmethod
    def get_by_id(visit_id):
        return db.session.get(
            Visit,
            visit_id,
        )

    @staticmethod
    def get_by_qr_token(token):
        return (
            Visit.query
            .filter(
                Visit.qr_token == token
            )
            .first()
        )

    @staticmethod
    def delete(visit):
        db.session.delete(visit)

    @staticmethod
    def search(search):

        query = (
            Visit.query
            .join(Visit.visitor)
        )

        if search:
            search = search.strip()

            query = query.filter(
                or_(
                    Visitor.first_name.ilike(
                        f"%{search}%"
                    ),
                    Visitor.middle_name.ilike(
                        f"%{search}%"
                    ),
                    Visitor.last_name.ilike(
                        f"%{search}%"
                    ),
                    Visitor.phone.ilike(
                        f"%{search}%"
                    ),
                    Visitor.email.ilike(
                        f"%{search}%"
                    ),
                    Visitor.id_number.ilike(
                        f"%{search}%"
                    ),
                    Visitor.passport_number.ilike(
                        f"%{search}%"
                    ),
                    Visitor.vehicle_registration.ilike(
                        f"%{search}%"
                    ),
                )
            )

        return (
            query
            .order_by(Visit.created_at.desc())
            .all()
        )

    @staticmethod
    def dashboard(
        status=None,
        site_id=None,
        visit_type=None,
        start_date=None,
        end_date=None,
    ):

        query = Visit.query

        if status:
            query = query.filter(
                Visit.status == status
            )

        if site_id:
            query = query.filter(
                Visit.site_id == site_id
            )

        if visit_type:
            query = query.filter(
                Visit.visit_type == visit_type
            )

        if start_date:
            query = query.filter(
                Visit.created_at >= start_date
            )

        if end_date:
            query = query.filter(
                Visit.created_at <= end_date
            )

        return (
            query
            .order_by(Visit.created_at.desc())
            .all()
        )