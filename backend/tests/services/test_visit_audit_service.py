import pytest

from app.common.database import DatabaseSession
from app.common.constants import VisitAuditAction
from app.common.exceptions import NotFoundError

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

from app.services.visit_audit_service import (
    VisitAuditService,
)
from app.services.visit_service import (
    VisitService,
)

from tests.factories.user_factory import UserFactory
from tests.factories.visitor_factory import VisitorFactory
from tests.factories.destination_factory import (
    DestinationFactory,
)

from app.common.constants import VisitType


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

    visit = VisitService.create({
        "visitor_id": visitor.id,
        "host_id": host.id,
        "destination_id": destination.id,
        "site_id": site.id,
        "visit_type": VisitType.PREBOOKED,
        "purpose": "Audit Test",
    })

    return visit, host


def test_create_visit_audit(
    session,
):

    visit, host = seed_visit()

    audit = VisitAuditService.create(
        visit_id=visit.id,
        action=VisitAuditAction.CREATED,
        user_id=host.id,
        notes="Visit created",
    )

    assert audit.id is not None
    assert audit.visit_id == visit.id
    assert audit.user_id == host.id
    assert audit.action == (
        VisitAuditAction.CREATED
    )
    assert audit.notes == "Visit created"


def test_get_visit_audits(
    session,
):

    visit, host = seed_visit()

    VisitAuditService.create(
        visit_id=visit.id,
        action=VisitAuditAction.CREATED,
        user_id=host.id,
    )

    VisitAuditService.create(
        visit_id=visit.id,
        action=VisitAuditAction.APPROVED,
        user_id=host.id,
        notes="Approved",
    )

    audits = (
        VisitAuditService
        .get_by_visit_id(visit.id)
    )

    assert len(audits) == 3

    actions = [
        audit.action
        for audit in audits
    ]

    assert VisitAuditAction.CREATED in actions
    assert VisitAuditAction.APPROVED in actions


def test_get_visit_audits_for_nonexistent_visit(
    session,
):

    with pytest.raises(
        NotFoundError
    ):
        VisitAuditService.get_by_visit_id(
            "11111111-1111-1111-1111-111111111111"
        )


def test_get_audit_by_id(
    session,
):

    visit, host = seed_visit()

    created = VisitAuditService.create(
        visit_id=visit.id,
        action=VisitAuditAction.CREATED,
        user_id=host.id,
    )

    found = VisitAuditService.get_by_id(
        created.id
    )

    assert found.id == created.id
    assert found.visit_id == visit.id
    assert found.action == (
        VisitAuditAction.CREATED
    )


def test_get_audit_by_id_not_found(
    session,
):

    with pytest.raises(
        NotFoundError
    ):
        VisitAuditService.get_by_id(
            "11111111-1111-1111-1111-111111111111"
        )