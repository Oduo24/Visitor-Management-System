import factory
from faker import Faker

from app.models.building import Building
from tests.factories.site_factory import SiteFactory

fake = Faker()


class BuildingFactory(factory.Factory):
    class Meta:
        model = Building

    site = factory.SubFactory(SiteFactory)

    site_id = factory.SelfAttribute("site.id")

    name = factory.Sequence(
        lambda n: f"Building {n}"
    )

    code = factory.Sequence(
        lambda n: f"BLD{n:03}"
    )

    description = factory.LazyFunction(
        fake.sentence
    )

    is_active = True