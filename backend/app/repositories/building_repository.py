from app.extensions import db
from app.models.building import Building


class BuildingRepository:

    @staticmethod
    def create(building):
        db.session.add(building)
        return building

    @staticmethod
    def get_all():
        return Building.query.order_by(Building.name).all()

    @staticmethod
    def get_by_id(building_id):
        return db.session.get(Building, building_id)

    @staticmethod
    def get_by_code(code):
        return Building.query.filter_by(code=code).first()

    @staticmethod
    def delete(building):
        db.session.delete(building)