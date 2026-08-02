from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository
from app.repositories.destination_repository import DestinationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.visitor_repository import VisitorRepository
from app.repositories.visit_repository import VisitRepository

from tests.factories.visit_factory import VisitFactory


def test_create_visit(session):

    visit = VisitFactory()

    OrganizationRepository.create(visit.host.organization)
    DepartmentRepository.create(visit.host.department)

    SiteRepository.create(visit.site)
    BuildingRepository.create(visit.destination.floor.building)
    FloorRepository.create(visit.destination.floor)
    DestinationRepository.create(visit.destination)

    UserRepository.create(visit.host)
    VisitorRepository.create(visit.visitor)

    VisitRepository.create(visit)

    DatabaseSession.commit()

    assert visit.id is not None


def test_get_all_visits(session):

    visit = VisitFactory()

    OrganizationRepository.create(visit.host.organization)
    DepartmentRepository.create(visit.host.department)

    SiteRepository.create(visit.site)
    BuildingRepository.create(visit.destination.floor.building)
    FloorRepository.create(visit.destination.floor)
    DestinationRepository.create(visit.destination)

    UserRepository.create(visit.host)
    VisitorRepository.create(visit.visitor)

    VisitRepository.create(visit)

    DatabaseSession.commit()

    visits = VisitRepository.get_all()

    assert len(visits) == 1


def test_get_visit_by_id(session):

    visit = VisitFactory()

    OrganizationRepository.create(visit.host.organization)
    DepartmentRepository.create(visit.host.department)

    SiteRepository.create(visit.site)
    BuildingRepository.create(visit.destination.floor.building)
    FloorRepository.create(visit.destination.floor)
    DestinationRepository.create(visit.destination)

    UserRepository.create(visit.host)
    VisitorRepository.create(visit.visitor)

    VisitRepository.create(visit)

    DatabaseSession.commit()

    found = VisitRepository.get_by_id(visit.id)

    assert found.id == visit.id


def test_delete_visit(session):

    visit = VisitFactory()

    OrganizationRepository.create(visit.host.organization)
    DepartmentRepository.create(visit.host.department)

    SiteRepository.create(visit.site)
    BuildingRepository.create(visit.destination.floor.building)
    FloorRepository.create(visit.destination.floor)
    DestinationRepository.create(visit.destination)

    UserRepository.create(visit.host)
    VisitorRepository.create(visit.visitor)

    VisitRepository.create(visit)

    DatabaseSession.commit()

    VisitRepository.delete(visit)

    DatabaseSession.commit()

    assert VisitRepository.get_by_id(visit.id) is None