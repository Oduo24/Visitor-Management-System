import factory

from app.models.destination import Destination
from tests.factories.floor_factory import FloorFactory


class DestinationFactory(factory.Factory):
    class Meta:
        model = Destination

    floor = factory.SubFactory(
        FloorFactory
    )

    floor_id = factory.SelfAttribute(
        "floor.id"
    )

    name = factory.Sequence(
        lambda n: f"Office {n}"
    )

    code = factory.Sequence(
        lambda n: f"DEST{n:03}"
    )

    is_active = True