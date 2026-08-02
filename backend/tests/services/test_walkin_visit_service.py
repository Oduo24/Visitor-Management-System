import pytest

from app.common.constants import VisitType

from app.services.walkin_visit_service import (
    WalkinVisitService,
)

from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.department_repository import (
    DepartmentRepository,
)
from app.repositories.site_repository import (
    SiteRepository,
)
from app.repositories.building_repository import (
    BuildingRepository,
)
from app.repositories.floor_repository import (
    FloorRepository,
)
from app.repositories.destination_repository import (
    DestinationRepository,
)
from app.repositories.user_repository import (
    UserRepository,
)
from app.repositories.visitor_repository import (
    VisitorRepository,
)

from app.common.database import DatabaseSession

from tests.factories.user_factory import UserFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.destination_factory import DestinationFactory


def test_create_walkin_visit(session):

    visitor = VisitorFactory()

    host = UserFactory()

    destination = DestinationFactory()

    site = destination.floor.building.site

    OrganizationRepository.create(
        host.organization
    )

    DepartmentRepository.create(
        host.department
    )

    SiteRepository.create(site)

    BuildingRepository.create(
        destination.floor.building
    )

    FloorRepository.create(
        destination.floor
    )

    DestinationRepository.create(
        destination
    )

    UserRepository.create(host)

    VisitorRepository.create(visitor)

    DatabaseSession.flush()

    visit = WalkinVisitService.create({

        "visitor_id": visitor.id,

        "host_id": host.id,

        "destination_id": destination.id,

        "site_id": site.id,

        "purpose": "Walk-in Visitor",

    })

    assert visit.visit_type == VisitType.WALK_IN

    assert visit.visitor_id == visitor.id

    assert visit.host_id == host.id