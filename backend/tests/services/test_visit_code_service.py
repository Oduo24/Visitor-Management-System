import pytest
 
from app.common.database import (
    DatabaseSession,
)
from app.common.exceptions import (
    NotFoundError,
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
 
from app.services.visit_code_service import (
    VisitCodeService,
)
from app.services.visit_service import (
    VisitService,
)
 
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
 
    site = (
        destination
        .floor
        .building
        .site
    )
 
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
        destination.floor.building
    )
 
    FloorRepository.create(
        destination.floor
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
 
    return VisitService.create({
        "visitor_id": visitor.id,
        "host_id": host.id,
        "destination_id": destination.id,
        "site_id": site.id,
        "visit_type": "PREBOOKED",
        "purpose": "Visitor code test",
    })
 
 
def test_generate_visitor_code(
    session,
):
 
    visit = seed_visit()
 
    code = (
        VisitCodeService.ensure_code(
            visit.id
        )
    )
 
    assert code is not None
    assert len(code) == 6
    assert code.isdigit()
 
    assert (
        int(code)
        >= 100000
    )
 
    assert (
        int(code)
        <= 999999
    )
 
    assert (
        visit.visitor_code
        == code
    )
 
    assert (
        visit.visitor_code_generated_at
        is not None
    )
 
 
def test_visitor_code_is_idempotent(
    session,
):
 
    visit = seed_visit()
 
    first = (
        VisitCodeService.ensure_code(
            visit.id
        )
    )
 
    second = (
        VisitCodeService.ensure_code(
            visit.id
        )
    )
 
    assert second == first
 
    assert (
        visit.visitor_code
        == first
    )
 
 
def test_get_visit_by_visitor_code(
    session,
):
 
    visit = seed_visit()
 
    code = (
        VisitCodeService.ensure_code(
            visit.id
        )
    )
 
    found = (
        VisitCodeService.get_by_code(
            code
        )
    )
 
    assert found.id == visit.id
 
 
def test_get_visit_by_invalid_code(
    session,
):
 
    with pytest.raises(
        NotFoundError,
        match="Invalid visitor code",
    ):
        VisitCodeService.get_by_code(
            "999999"
        )
 
 
def test_generate_code_visit_not_found(
    session,
):
 
    with pytest.raises(
        NotFoundError,
        match="Visit not found",
    ):
        VisitCodeService.ensure_code(
            (
                "00000000-0000-0000-"
                "0000-000000000000"
            )
        )