import factory

from app.models.user import User

from tests.factories.organization_factory import (
    OrganizationFactory,
)
from tests.factories.department_factory import (
    DepartmentFactory,
)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    organization = factory.SubFactory(
        OrganizationFactory
    )

    department = factory.SubFactory(
        DepartmentFactory,
        organization=factory.SelfAttribute("..organization"),
        organization_id=factory.SelfAttribute(
            "..organization.id"
        ),
    )

    organization_id = factory.SelfAttribute(
        "organization.id"
    )

    department_id = factory.SelfAttribute(
        "department.id"
    )

    first_name = factory.Sequence(
        lambda n: f"John{n}"
    )

    last_name = "Doe"

    email = factory.Sequence(
        lambda n: f"john{n}@example.com"
    )

    phone = "0712345678"

    employee_number = factory.Sequence(
        lambda n: f"EMP{n:04}"
    )

    job_title = "ICT Officer"

    profile_photo_url = (
        "https://example.com/photo.jpg"
    )

    password_hash = (
        "pbkdf2:sha256:testhash"
    )

    is_active = True