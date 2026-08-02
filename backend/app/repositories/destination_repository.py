from app.extensions import db
from app.models.destination import Destination


class DestinationRepository:

    @staticmethod
    def create(destination):
        db.session.add(destination)
        return destination

    @staticmethod
    def get_all():
        return Destination.query.order_by(
            Destination.name
        ).all()

    @staticmethod
    def get_by_id(destination_id):
        return db.session.get(
            Destination,
            destination_id,
        )

    @staticmethod
    def get_by_code(code):
        return Destination.query.filter_by(
            code=code
        ).first()

    @staticmethod
    def delete(destination):
        db.session.delete(destination)