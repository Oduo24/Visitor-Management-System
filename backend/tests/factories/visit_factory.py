import factory

from tests.factories.user_factory import UserFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.destination_factory import DestinationFactory

from app.models.visit import Visit

from app.common.constants import VisitType, VisitStatus


class VisitFactory(factory.Factory):

    class Meta:
        model = Visit

    visitor = factory.SubFactory(
        VisitorFactory
    )

    host = factory.SubFactory(
        UserFactory
    )

    destination = factory.SubFactory(
        DestinationFactory
    )

    site = factory.SelfAttribute(
        "destination.floor.building.site"
    )

    visit_type = VisitType.PREBOOKED

    status = VisitStatus.PENDING

    purpose = factory.Faker("sentence")

    