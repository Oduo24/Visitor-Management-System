from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError

from app.models.floor import Floor

from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository


class FloorService:

    @staticmethod
    def create(data):
        building = BuildingRepository.get_by_id(
            data["building_id"]
        )

        if not building:
            raise NotFoundError("Building not found.")

        existing = FloorRepository.get_by_building_and_level(
            data["building_id"],
            data["level"],
        )

        if existing:
            raise ConflictError(
                "Floor level already exists for this building."
            )

        floor = Floor(
            building_id=data["building_id"],
            name=data["name"],
            level=data["level"],
            is_active=data.get("is_active", True),
        )

        FloorRepository.create(floor)
        DatabaseSession.commit()

        return floor

    @staticmethod
    def get_all():
        return FloorRepository.get_all()

    @staticmethod
    def get_by_id(floor_id):
        floor = FloorRepository.get_by_id(floor_id)

        if not floor:
            raise NotFoundError("Floor not found.")

        return floor

    @staticmethod
    def update(floor_id, data):
        floor = FloorRepository.get_by_id(floor_id)

        if not floor:
            raise NotFoundError("Floor not found.")

        if "building_id" in data:
            building = BuildingRepository.get_by_id(
                data["building_id"]
            )

            if not building:
                raise NotFoundError("Building not found.")

            floor.building_id = data["building_id"]

        if (
            "level" in data
            and data["level"] != floor.level
        ):
            existing = FloorRepository.get_by_building_and_level(
                floor.building_id,
                data["level"],
            )

            if existing:
                raise ConflictError(
                    "Floor level already exists for this building."
                )

            floor.level = data["level"]

        floor.name = data.get("name", floor.name)
        floor.is_active = data.get(
            "is_active",
            floor.is_active,
        )

        DatabaseSession.commit()

        return floor

    @staticmethod
    def delete(floor_id):
        floor = FloorRepository.get_by_id(floor_id)

        if not floor:
            raise NotFoundError("Floor not found.")

        FloorRepository.delete(floor)
        DatabaseSession.commit()