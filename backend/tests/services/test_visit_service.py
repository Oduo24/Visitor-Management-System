import pytest

from app.common.database import DatabaseSession
from app.common.exceptions import NotFoundError

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.floor_repository import FloorRepository
from app.repositories.destination_repository import DestinationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.visitor_repository import VisitorRepository
from app.models.visit import Visit
from app.common.constants import VisitType

from tests.factories.user_factory import UserFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.destination_factory import DestinationFactory

from app.services.visit_service import VisitService

from tests.factories.visit_factory import VisitFactory


def test_get_all_visits(session):

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

    VisitService.create({
        "visitor_id": visitor.id,
        "host_id": host.id,
        "destination_id": destination.id,
        "site_id": site.id,
        "visit_type": VisitType.PREBOOKED,
        "purpose": "Test Visit",
    })

    visits = VisitService.get_all()

    assert len(visits) == 1
    assert visits[0].visitor_id == visitor.id
    assert visits[0].host_id == host.id
    assert visits[0].destination_id == destination.id


def test_get_visit(session):

    visit = VisitFactory()

    OrganizationRepository.create(visit.host.organization)
    DepartmentRepository.create(visit.host.department)

    SiteRepository.create(visit.site)
    BuildingRepository.create(visit.destination.floor.building)
    FloorRepository.create(visit.destination.floor)
    DestinationRepository.create(visit.destination)

    UserRepository.create(visit.host)
    VisitorRepository.create(visit.visitor)

    DatabaseSession.flush()

    created = VisitService.create({
        "visitor_id": visit.visitor.id,
        "host_id": visit.host.id,
        "destination_id": visit.destination.id,
        "site_id": visit.site.id,
        "visit_type": visit.visit_type,
        "purpose": visit.purpose,
    })

    DatabaseSession.commit()

    found = VisitService.get_by_id(created.id)

    assert found.id == created.id


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

    DatabaseSession.flush()

    created = VisitService.create({
        "visitor_id": visit.visitor.id,
        "host_id": visit.host.id,
        "destination_id": visit.destination.id,
        "site_id": visit.site.id,
        "visit_type": visit.visit_type,
        "purpose": visit.purpose,
    })

    DatabaseSession.commit()

    VisitService.delete(created.id)

    with pytest.raises(NotFoundError):
        VisitService.get_by_id(created.id)


def test_get_visit_not_found(session):

    with pytest.raises(NotFoundError):
        VisitService.get_by_id(
            "11111111-1111-1111-1111-111111111111"
        )