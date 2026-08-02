from app.extensions import db

from app.models.visitor import Visitor


class VisitorRepository:

    @staticmethod
    def create(visitor):
        db.session.add(visitor)
        return visitor

    @staticmethod
    def get_all():
        return (
            Visitor.query
            .order_by(
                Visitor.first_name,
                Visitor.last_name,
            )
            .all()
        )

    @staticmethod
    def get_by_id(visitor_id):
        return db.session.get(
            Visitor,
            visitor_id,
        )

    @staticmethod
    def get_by_email(email):
        return (
            Visitor.query
            .filter_by(email=email)
            .first()
        )

    @staticmethod
    def get_by_phone(phone):
        return (
            Visitor.query
            .filter_by(phone=phone)
            .first()
        )

    @staticmethod
    def get_by_id_number(id_number):
        return (
            Visitor.query
            .filter_by(id_number=id_number)
            .first()
        )

    @staticmethod
    def get_by_passport_number(passport_number):
        return (
            Visitor.query
            .filter_by(passport_number=passport_number)
            .first()
        )

    @staticmethod
    def search(query):

        search = f"%{query}%"

        return (
            Visitor.query.filter(
                (Visitor.first_name.ilike(search))
                | (Visitor.last_name.ilike(search))
                | (Visitor.email.ilike(search))
                | (Visitor.phone.ilike(search))
                | (Visitor.company.ilike(search))
                | (Visitor.id_number.ilike(search))
                | (Visitor.passport_number.ilike(search))
            )
            .order_by(
                Visitor.first_name,
                Visitor.last_name,
            )
            .all()
        )

    @staticmethod
    def delete(visitor):
        db.session.delete(visitor)