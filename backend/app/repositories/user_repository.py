from app.extensions import db
from app.models.user import User


class UserRepository:

    @staticmethod
    def create(user):
        db.session.add(user)
        return user

    @staticmethod
    def get_all():
        return User.query.order_by(
            User.first_name,
            User.last_name,
        ).all()

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(
            User,
            user_id,
        )

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(
            email=email
        ).first()

    @staticmethod
    def get_by_employee_number(employee_number):
        return User.query.filter_by(
            employee_number=employee_number
        ).first()

    @staticmethod
    def delete(user):
        db.session.delete(user)

    @staticmethod
    def exists(user_id):
        return (
            User.query.filter_by(id=user_id)
            .first()
            is not None
        )