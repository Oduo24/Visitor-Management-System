import factory

from app.models.user_site_role import UserSiteRole

from tests.factories.user_factory import UserFactory
from tests.factories.site_factory import SiteFactory
from tests.factories.role_factory import RoleFactory


class UserSiteRoleFactory(factory.Factory):
    class Meta:
        model = UserSiteRole

    user = factory.SubFactory(UserFactory)

    site = factory.SubFactory(
        SiteFactory,
        organization=factory.SelfAttribute(
            "..user.organization"
        ),
        organization_id=factory.SelfAttribute(
            "..user.organization.id"
        ),
    )

    role = factory.SubFactory(
        RoleFactory,
        organization=factory.SelfAttribute(
            "..user.organization"
        ),
        organization_id=factory.SelfAttribute(
            "..user.organization.id"
        ),
    )

    user_id = factory.SelfAttribute(
        "user.id"
    )

    site_id = factory.SelfAttribute(
        "site.id"
    )

    role_id = factory.SelfAttribute(
        "role.id"
    )