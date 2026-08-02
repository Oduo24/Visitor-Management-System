import factory

from app.models.department import Department
from tests.factories.organization_factory import OrganizationFactory


class DepartmentFactory(factory.Factory):
    class Meta:
        model = Department

    organization = factory.SubFactory(
        OrganizationFactory
    )

    organization_id = factory.SelfAttribute(
        "organization.id"
    )

    name = factory.Sequence(
        lambda n: f"Department {n}"
    )

    code = factory.Sequence(
        lambda n: f"DEPT{n:03}"
    )

    description = factory.Sequence(
        lambda n: f"Department Description {n}"
    )

    is_active = True