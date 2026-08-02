from app.extensions import db
from app.models.floor import Floor


class FloorRepository:

    @staticmethod
    def create(floor):
        db.session.add(floor)
        return floor

    @staticmethod
    def get_all():
        return Floor.query.order_by(Floor.level).all()

    @staticmethod
    def get_by_id(floor_id):
        return db.session.get(Floor, floor_id)

    @staticmethod
    def get_by_building_and_level(building_id, level):
        return Floor.query.filter_by(
            building_id=building_id,
            level=level,
        ).first()

    @staticmethod
    def delete(floor):
        db.session.delete(floor)