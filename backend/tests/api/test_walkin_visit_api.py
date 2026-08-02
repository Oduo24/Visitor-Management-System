from app.common.constants import VisitType

from app.common.database import DatabaseSession

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

from tests.factories.user_factory import UserFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.destination_factory import DestinationFactory


def seed_dependencies():

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

    return visitor, host, destination, site


def test_create_walkin_visit(
    client,
    session,
    auth_headers,
):

    visitor, host, destination, site = seed_dependencies()

    payload = {

        "visitor_id": visitor.id,

        "host_id": host.id,

        "destination_id": destination.id,

        "site_id": site.id,

        "purpose": "Walk-in Visitor",

    }

    response = client.post(
        "/api/walkin-visits",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 201

    body = response.get_json()

    assert body["success"] is True

    assert (
        body["data"]["visit_type"]
        == VisitType.WALK_IN
    )