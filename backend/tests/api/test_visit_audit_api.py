from app.common.constants import (
    VisitAuditAction,
)

from app.services.visit_audit_service import (
    VisitAuditService,
)

from app.services.visit_service import (
    VisitService,
)
from tests.api.test_visit_checkout_api import seed_visit


def test_get_visit_audit(
    client,
    session,
    auth_headers_factory,
):

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    visit = seed_visit()

    VisitAuditService.create(
        visit_id=visit.id,
        action=VisitAuditAction.APPROVED,
        user_id=visit.host_id,
        notes="Approved",
    )

    VisitAuditService.create(
        visit_id=visit.id,
        action=VisitAuditAction.BADGE_ISSUED,
        notes="Badge issued",
    )

    # Explicitly commit because these audit
    # records are being created directly by
    # the test rather than through a lifecycle
    # service.
    from app.common.database import (
        DatabaseSession,
    )

    DatabaseSession.commit()

    response = client.get(
        f"/api/visits/{visit.id}/audit",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert len(data) >= 2

    actions = [
        audit["action"]
        for audit in data
    ]

    assert VisitAuditAction.APPROVED in actions
    assert (
        VisitAuditAction.BADGE_ISSUED
        in actions
    )


def test_get_visit_audit_not_found(
    client,
    session,
    auth_headers_factory,
):

    import uuid

    headers = auth_headers_factory(
        "ORG_ADMIN"
    )

    response = client.get(
        f"/api/visits/{uuid.uuid4()}/audit",
        headers=headers,
    )

    assert response.status_code == 404


def test_get_visit_audit_requires_authentication(
    client,
    session,
):

    visit = seed_visit()

    response = client.get(
        f"/api/visits/{visit.id}/audit"
    )

    assert response.status_code == 401