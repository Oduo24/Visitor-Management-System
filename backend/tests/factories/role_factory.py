import factory

from app.models.role import Role
from tests.factories.organization_factory import OrganizationFactory


class RoleFactory(factory.Factory):
    class Meta:
        model = Role

    organization = factory.SubFactory(
        OrganizationFactory
    )

    organization_id = factory.SelfAttribute(
        "organization.id"
    )

    name = factory.Sequence(
        lambda n: f"Role {n}"
    )

    code = factory.Sequence(
        lambda n: f"ROLE{n:03}"
    )

    description = factory.Sequence(
        lambda n: f"Role Description {n}"
    )

    is_active = True