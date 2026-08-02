import pytest

from app.common.constants import VisitType, VisitStatus
from app.common.exceptions import NotFoundError

from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository
from app.repositories.destination_repository import DestinationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.visitor_repository import VisitorRepository

from app.services.prebook_visit_service import PrebookVisitService

from tests.factories.visitor_factory import VisitorFactory
from tests.factories.user_factory import UserFactory
from tests.factories.destination_factory import DestinationFactory


def setup_dependencies():

    visitor = VisitorFactory()
    host = UserFactory()
    destination = DestinationFactory()
    site = destination.floor.building.site

    OrganizationRepository.create(host.organization)
    DepartmentRepository.create(host.department)

    SiteRepository.create(site)
    BuildingRepository.create(destination.floor.building)
    FloorRepository.create(destination.floor)
    DestinationRepository.create(destination)

    UserRepository.create(host)
    VisitorRepository.create(visitor)

    DatabaseSession.flush()

    return visitor, host, destination, site


def test_create_prebook_visit(session):

    visitor, host, destination, site = setup_dependencies()

    visit = PrebookVisitService.create({
        "visitor_id": visitor.id,
        "host_id": host.id,
        "destination_id": destination.id,
        "site_id": site.id,
        "visit_type": VisitType.PREBOOKED,
        "purpose": "Business Meeting",
    })

    assert visit.id is not None
    assert visit.visit_type == VisitType.PREBOOKED
    assert visit.status == VisitStatus.PENDING
    assert visit.visitor_id == visitor.id
    assert visit.host_id == host.id


def test_create_prebook_visitor_not_found(session):

    visitor, host, destination, site = setup_dependencies()

    with pytest.raises(NotFoundError):

        PrebookVisitService.create({
            "visitor_id": "11111111-1111-1111-1111-111111111111",
            "host_id": host.id,
            "destination_id": destination.id,
            "site_id": site.id,
            "visit_type": VisitType.PREBOOKED,
        })


def test_create_prebook_host_not_found(session):

    visitor, host, destination, site = setup_dependencies()

    with pytest.raises(NotFoundError):

        PrebookVisitService.create({
            "visitor_id": visitor.id,
            "host_id": "11111111-1111-1111-1111-111111111111",
            "destination_id": destination.id,
            "site_id": site.id,
            "visit_type": VisitType.PREBOOKED,
        })