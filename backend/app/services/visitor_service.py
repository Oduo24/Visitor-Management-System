from app.common.database import DatabaseSession
from app.common.exceptions import (
    ConflictError,
    NotFoundError,
)

from app.models.visitor import Visitor

from app.repositories.visitor_repository import VisitorRepository


class VisitorService:

    @staticmethod
    def get_all():
        return VisitorRepository.get_all()

    @staticmethod
    def get_by_id(visitor_id):

        visitor = VisitorRepository.get_by_id(
            visitor_id
        )

        if not visitor:
            raise NotFoundError(
                "Visitor not found."
            )

        return visitor

    @staticmethod
    def search(query):
        return VisitorRepository.search(query)

    @staticmethod
    def create(data):

        if (
            data.get("id_number")
            and VisitorRepository.get_by_id_number(
                data["id_number"]
            )
        ):
            raise ConflictError(
                "ID number already exists."
            )

        if (
            data.get("passport_number")
            and VisitorRepository.get_by_passport_number(
                data["passport_number"]
            )
        ):
            raise ConflictError(
                "Passport number already exists."
            )

        visitor = Visitor(**data)

        VisitorRepository.create(visitor)

        DatabaseSession.commit()

        return visitor

    @staticmethod
    def update(visitor_id, data):

        visitor = VisitorService.get_by_id(
            visitor_id
        )

        if (
            "id_number" in data
            and data["id_number"] != visitor.id_number
        ):
            existing = VisitorRepository.get_by_id_number(
                data["id_number"]
            )

            if existing:
                raise ConflictError(
                    "ID number already exists."
                )

        if (
            "passport_number" in data
            and data["passport_number"] != visitor.passport_number
        ):
            existing = (
                VisitorRepository.get_by_passport_number(
                    data["passport_number"]
                )
            )

            if existing:
                raise ConflictError(
                    "Passport number already exists."
                )

        for key, value in data.items():
            setattr(
                visitor,
                key,
                value,
            )

        DatabaseSession.commit()

        return visitor

    @staticmethod
    def delete(visitor_id):

        visitor = VisitorService.get_by_id(
            visitor_id
        )

        VisitorRepository.delete(visitor)

        DatabaseSession.commit()