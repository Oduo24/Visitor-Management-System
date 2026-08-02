from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError

from app.models.destination import Destination

from app.repositories.floor_repository import FloorRepository
from app.repositories.destination_repository import (
    DestinationRepository,
)


class DestinationService:

    @staticmethod
    def create(data):
        floor = FloorRepository.get_by_id(
            data["floor_id"]
        )

        if not floor:
            raise NotFoundError("Floor not found.")

        if data.get("code"):
            existing = DestinationRepository.get_by_code(
                data["code"]
            )

            if existing:
                raise ConflictError(
                    "Destination code already exists."
                )

        destination = Destination(
            floor_id=data["floor_id"],
            name=data["name"],
            code=data.get("code"),
            is_active=data.get(
                "is_active",
                True,
            ),
        )

        DestinationRepository.create(destination)
        DatabaseSession.commit()

        return destination

    @staticmethod
    def get_all():
        return DestinationRepository.get_all()

    @staticmethod
    def get_by_id(destination_id):
        destination = DestinationRepository.get_by_id(
            destination_id
        )

        if not destination:
            raise NotFoundError(
                "Destination not found."
            )

        return destination

    @staticmethod
    def update(destination_id, data):
        destination = DestinationRepository.get_by_id(
            destination_id
        )

        if not destination:
            raise NotFoundError(
                "Destination not found."
            )

        if (
            "floor_id" in data
            and data["floor_id"] != destination.floor_id
        ):
            floor = FloorRepository.get_by_id(
                data["floor_id"]
            )

            if not floor:
                raise NotFoundError(
                    "Floor not found."
                )

            destination.floor_id = data["floor_id"]

        if (
            "code" in data
            and data["code"] != destination.code
        ):
            existing = DestinationRepository.get_by_code(
                data["code"]
            )

            if existing:
                raise ConflictError(
                    "Destination code already exists."
                )

            destination.code = data["code"]

        destination.name = data.get(
            "name",
            destination.name,
        )

        destination.is_active = data.get(
            "is_active",
            destination.is_active,
        )

        DatabaseSession.commit()

        return destination

    @staticmethod
    def delete(destination_id):
        destination = DestinationRepository.get_by_id(
            destination_id
        )

        if not destination:
            raise NotFoundError(
                "Destination not found."
            )

        DestinationRepository.delete(destination)
        DatabaseSession.commit()