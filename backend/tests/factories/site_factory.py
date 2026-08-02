import factory
from faker import Faker

from app.models.site import Site
from tests.factories.organization_factory import OrganizationFactory

fake = Faker()


class SiteFactory(factory.Factory):
    class Meta:
        model = Site

    organization = factory.SubFactory(OrganizationFactory)

    organization_id = factory.SelfAttribute("organization.id")

    name = factory.Sequence(
        lambda n: f"Head Office {n}"
    )

    code = factory.Sequence(
        lambda n: f"SITE{n:03}"
    )

    address = factory.LazyFunction(
        fake.street_address
    )

    city = factory.LazyFunction(
        fake.city
    )

    country = factory.LazyFunction(
        fake.country
    )

    phone = factory.LazyFunction(
        fake.phone_number
    )

    email = factory.LazyFunction(
        fake.company_email
    )

    is_active = True