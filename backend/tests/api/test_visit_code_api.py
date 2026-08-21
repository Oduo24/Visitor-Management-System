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
 
from app.services.visit_service import (
    VisitService,
)
 
from app.services.visit_code_service import VisitCodeService
from tests.factories.destination_factory import (
    DestinationFactory,
)
from tests.factories.user_factory import (
    UserFactory,
)
from tests.factories.visitor_factory import (
    VisitorFactory,
)
 
 
def seed_visit():
 
    visitor = VisitorFactory()
    host = UserFactory()
    destination = DestinationFactory()
 
    floor = destination.floor
    building = floor.building
    site = building.site
 
    OrganizationRepository.create(
        host.organization
    )
 
    DepartmentRepository.create(
        host.department
    )
 
    SiteRepository.create(
        site
    )
 
    BuildingRepository.create(
        building
    )
 
    FloorRepository.create(
        floor
    )
 
    DestinationRepository.create(
        destination
    )
 
    UserRepository.create(
        host
    )
 
    VisitorRepository.create(
        visitor
    )
 
    DatabaseSession.flush()
 
    visit = VisitService.create({
        "visitor_id": visitor.id,
        "host_id": host.id,
        "destination_id": destination.id,
        "site_id": site.id,
        "visit_type": "PREBOOKED",
        "purpose": "Visitor code test",
    })
 
    return visit



def test_get_visit_by_visitor_code(
    client,
    session,
    auth_headers_factory,
):
 
    visit = seed_visit()
 
    code = (
        VisitCodeService.ensure_code(
            visit.id
        )
    )
 
    headers = (
        auth_headers_factory(
            "ORG_ADMIN"
        )
    )
 
    response = client.get(
        f"/api/visits/code/{code}",
        headers=headers,
    )
 
    assert response.status_code == 200
 
    data = response.get_json()["data"]
 
    assert (
        data["id"]
        == str(visit.id)
    )
 
    assert (
        data["visitor_code"]
        == code
    )
 
 
def test_get_visit_by_invalid_visitor_code(
    client,
    session,
    auth_headers_factory,
):
 
    headers = (
        auth_headers_factory(
            "ORG_ADMIN"
        )
    )
 
    response = client.get(
        "/api/visits/code/999999",
        headers=headers,
    )
 
    assert response.status_code == 404
 
 
def test_get_visit_by_code_requires_authentication(
    client,
    session,
):
 
    response = client.get(
        "/api/visits/code/123456"
    )
 
    assert response.status_code == 401