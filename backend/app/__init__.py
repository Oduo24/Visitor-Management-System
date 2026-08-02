from flask import Flask

from app.config import Config
from app.extensions import db, migrate, jwt, cors
from app.common.handlers import register_error_handlers


def create_app(config_class=None):
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    register_error_handlers(app)

    from app.common.jwt import register_jwt_callbacks

    register_jwt_callbacks(jwt)

    # Import models so Alembic can detect them
    from app import models

    # Register blueprints
    from app.api.health import health_bp
    from app.api.organizations import organization_bp
    from app.api.sites import site_bp
    from app.api.buildings import building_bp
    from app.api.floors import floor_bp
    from app.api.destinations import destination_bp
    from app.api.departments import department_bp
    from app.api.roles import role_bp
    from app.api.users import user_bp
    from app.api.user_site_roles import user_site_role_bp
    from app.api.auth import auth_bp
    from app.api.hosts import host_bp
    from app.api.visitors import visitor_bp
 

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(organization_bp, url_prefix="/api/organizations")
    app.register_blueprint(site_bp, url_prefix="/api/sites")
    app.register_blueprint(building_bp, url_prefix="/api/buildings")
    app.register_blueprint(floor_bp, url_prefix="/api/floors")
    app.register_blueprint(destination_bp, url_prefix="/api/destinations")
    app.register_blueprint(department_bp, url_prefix="/api/departments")
    app.register_blueprint(role_bp, url_prefix="/api/roles")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(user_site_role_bp, url_prefix="/api/user-site-roles")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(host_bp, url_prefix="/api/hosts")
    app.register_blueprint(visitor_bp, url_prefix="/api/visitors")


    return app