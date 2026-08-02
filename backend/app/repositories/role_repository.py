from app.extensions import db
from app.models.role import Role


class RoleRepository:

    @staticmethod
    def create(role):
        db.session.add(role)
        return role

    @staticmethod
    def get_all():
        return Role.query.order_by(
            Role.name
        ).all()

    @staticmethod
    def get_by_id(role_id):
        return db.session.get(
            Role,
            role_id,
        )

    @staticmethod
    def get_by_code(code):
        return Role.query.filter_by(
            code=code
        ).first()

    @staticmethod
    def delete(role):
        db.session.delete(role)