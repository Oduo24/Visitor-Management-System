import factory

from app.models.floor import Floor
from tests.factories.building_factory import BuildingFactory


class FloorFactory(factory.Factory):
    class Meta:
        model = Floor

    building = factory.SubFactory(BuildingFactory)

    building_id = factory.SelfAttribute("building.id")

    name = factory.Sequence(
        lambda n: f"Floor {n}"
    )

    level = factory.Sequence(
        lambda n: n
    )

    is_active = True