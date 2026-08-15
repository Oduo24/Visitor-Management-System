import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from app.config import TestingConfig
from app.extensions import db

from app.common.database import DatabaseSession

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.site_repository import SiteRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_site_role_repository import UserSiteRoleRepository

from tests.factories.user_site_role_factory import UserSiteRoleFactory
from app.seeders.database_seeder import DatabaseSeeder


@pytest.fixture(scope="session")
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def session(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        yield db.session

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app, session):
    return app.test_client()


@pytest.fixture
def seeded_user_id(app):

    with app.app_context():

        data = DatabaseSeeder.run()

        return str(data["user"].id)


@pytest.fixture
def auth_headers(app, seeded_user_id):

    with app.app_context():

        token = create_access_token(
            identity=seeded_user_id
        )

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def auth_headers_factory(app):

    def _factory(role_code):

        data = DatabaseSeeder.run()

        data["role"].code = role_code

        DatabaseSession.commit()

        with app.app_context():

            token = create_access_token(
                identity=data["user"].id
            )

        return {
            "Authorization": f"Bearer {token}"
        }

    return _factory



