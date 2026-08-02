import pytest

from app.common.exceptions import (
    ConflictError,
    NotFoundError,
)

from app.common.database import DatabaseSession

from app.repositories.visitor_repository import VisitorRepository

from app.services.visitor_service import VisitorService

from tests.factories.visitor_factory import VisitorFactory


def test_create_visitor(session):

    visitor = VisitorFactory()

    created = VisitorService.create({

        "first_name": visitor.first_name,
        "middle_name": visitor.middle_name,
        "last_name": visitor.last_name,
        "gender": visitor.gender,
        "date_of_birth": visitor.date_of_birth,
        "email": visitor.email,
        "phone": visitor.phone,
        "company": visitor.company,
        "address": visitor.address,
        "nationality": visitor.nationality,
        "id_number": visitor.id_number,
        "passport_number": visitor.passport_number,
        "vehicle_registration": visitor.vehicle_registration,
        "photo_url": visitor.photo_url,
        "notes": visitor.notes,

    })

    assert created.id is not None


def test_duplicate_id_number(session):

    visitor = VisitorFactory()

    VisitorRepository.create(visitor)

    DatabaseSession.commit()

    with pytest.raises(ConflictError):

        VisitorService.create({

            "first_name": "Jane",
            "last_name": "Doe",
            "phone": "0700000000",
            "id_number": visitor.id_number,

        })


def test_get_visitor_not_found(session):

    with pytest.raises(NotFoundError):

        VisitorService.get_by_id(
            "11111111-1111-1111-1111-111111111111"
        )


def test_delete_visitor(session):

    visitor = VisitorFactory()

    VisitorRepository.create(visitor)

    DatabaseSession.commit()

    VisitorService.delete(
        visitor.id
    )

    with pytest.raises(NotFoundError):

        VisitorService.get_by_id(
            visitor.id
        )