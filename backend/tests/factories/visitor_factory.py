import factory
from faker import Faker

from app.models.visitor import Visitor

fake = Faker()


class VisitorFactory(factory.Factory):

    class Meta:
        model = Visitor

    first_name = factory.LazyFunction(
        fake.first_name
    )

    middle_name = factory.LazyFunction(
        fake.first_name
    )

    last_name = factory.LazyFunction(
        fake.last_name
    )

    gender = factory.Iterator(
        [
            "Male",
            "Female",
        ]
    )

    date_of_birth = factory.LazyFunction(
        fake.date_of_birth
    )

    email = factory.LazyFunction(
        fake.email
    )

    phone = factory.LazyFunction(
        fake.phone_number
    )

    company = factory.LazyFunction(
        fake.company
    )

    address = factory.LazyFunction(
        fake.address
    )

    nationality = factory.LazyFunction(
        fake.country
    )

    id_number = factory.Sequence(
        lambda n: f"ID{100000+n}"
    )

    passport_number = factory.Sequence(
        lambda n: f"P{100000+n}"
    )

    vehicle_registration = factory.Sequence(
        lambda n: f"KDA {100+n}A"
    )

    photo_url = factory.LazyFunction(
        fake.image_url
    )

    is_blacklisted = False

    notes = factory.LazyFunction(
        fake.sentence
    )