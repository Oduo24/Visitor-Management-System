from app.common.database import DatabaseSession
from app.common.exceptions import ConflictError, NotFoundError
from app.models.building import Building
from app.repositories.building_repository import BuildingRepository
from app.repositories.site_repository import SiteRepository


class BuildingService:

    @staticmethod
    def create(data):
        site = SiteRepository.get_by_id(data["site_id"])

        if not site:
            raise NotFoundError("Site not found.")

        existing = BuildingRepository.get_by_code(data["code"])

        if existing:
            raise ConflictError("Building code already exists.")

        building = Building(
            site_id=data["site_id"],
            name=data["name"],
            code=data["code"],
            description=data.get("description"),
            is_active=data.get("is_active", True),
        )

        BuildingRepository.create(building)
        DatabaseSession.commit()

        return building

    @staticmethod
    def get_all():
        return BuildingRepository.get_all()

    @staticmethod
    def get_by_id(building_id):
        building = BuildingRepository.get_by_id(building_id)

        if not building:
            raise NotFoundError("Building not found.")

        return building

    @staticmethod
    def update(building_id, data):
        building = BuildingRepository.get_by_id(building_id)

        if not building:
            raise NotFoundError("Building not found.")

        if (
            "site_id" in data
            and data["site_id"] != building.site_id
        ):
            site = SiteRepository.get_by_id(data["site_id"])

            if not site:
                raise NotFoundError("Site not found.")

            building.site_id = data["site_id"]

        if (
            "code" in data
            and data["code"] != building.code
        ):
            existing = BuildingRepository.get_by_code(data["code"])

            if existing:
                raise ConflictError("Building code already exists.")

            building.code = data["code"]

        building.name = data.get("name", building.name)
        building.description = data.get(
            "description",
            building.description,
        )
        building.is_active = data.get(
            "is_active",
            building.is_active,
        )

        DatabaseSession.commit()

        return building

    @staticmethod
    def delete(building_id):
        building = BuildingRepository.get_by_id(building_id)

        if not building:
            raise NotFoundError("Building not found.")

        BuildingRepository.delete(building)
        DatabaseSession.commit()