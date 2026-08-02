from app.extensions import db
from app.models.user_site_role import UserSiteRole


class UserSiteRoleRepository:

    @staticmethod
    def create(user_site_role):
        db.session.add(user_site_role)
        return user_site_role

    @staticmethod
    def get_all():
        return UserSiteRole.query.all()

    @staticmethod
    def get_by_id(record_id):
        return db.session.get(
            UserSiteRole,
            record_id,
        )

    @staticmethod
    def get_by_user_site_role(
        user_id,
        site_id,
        role_id,
    ):
        return UserSiteRole.query.filter_by(
            user_id=user_id,
            site_id=site_id,
            role_id=role_id,
        ).first()

    @staticmethod
    def delete(record):
        db.session.delete(record)