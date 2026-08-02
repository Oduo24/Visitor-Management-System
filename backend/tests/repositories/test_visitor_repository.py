from app.common.database import DatabaseSession

from app.repositories.visitor_repository import VisitorRepository

from tests.factories.visitor_factory import VisitorFactory


def test_create_visitor(session):

    visitor = VisitorFactory()

    VisitorRepository.create(visitor)

    DatabaseSession.commit()

    assert visitor.id is not None


def test_get_visitor_by_id(session):

    visitor = VisitorFactory()

    VisitorRepository.create(visitor)

    DatabaseSession.commit()

    found = VisitorRepository.get_by_id(
        visitor.id
    )

    assert found.id == visitor.id


def test_search_visitors(session):

    visitor = VisitorFactory(
        first_name="John"
    )

    VisitorRepository.create(visitor)

    DatabaseSession.commit()

    results = VisitorRepository.search(
        "John"
    )

    assert len(results) == 1