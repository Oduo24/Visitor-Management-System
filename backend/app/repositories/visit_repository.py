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
    def delete(visit):
        db.session.delete(visit)

    @staticmethod
    def search(search):

        return (
            Visit.query
            .join(Visit.visitor)
            .filter(
                Visit.visitor.has(
                    Visitor.first_name.ilike(f"%{search}%")
                )
            )
            .all()
        )