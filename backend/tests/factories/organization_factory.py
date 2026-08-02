import factory
from faker import Faker

from app.models.organization import Organization

fake = Faker()


class OrganizationFactory(factory.Factory):
    class Meta:
        model = Organization

    name = factory.LazyFunction(fake.company)

    code = factory.Sequence(
        lambda n: f"ORG{n:04}"
    )

    email = factory.LazyFunction(fake.company_email)

    phone = factory.LazyFunction(fake.phone_number)

    website = factory.LazyAttribute(
        lambda obj: f"https://{obj.code.lower()}.com"
    )

    logo_url = factory.LazyFunction(
        lambda: fake.image_url()
    )

    description = factory.LazyFunction(
        fake.catch_phrase
    )

    is_active = True