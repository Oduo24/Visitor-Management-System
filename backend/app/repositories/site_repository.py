from app.extensions import db
from app.models.site import Site


class SiteRepository:

    @staticmethod
    def create(site):
        db.session.add(site)
        return site

    @staticmethod
    def get_all():
        return Site.query.order_by(Site.name).all()

    @staticmethod
    def get_by_id(site_id):
        return db.session.get(Site, site_id)

    @staticmethod
    def get_by_code(code):
        return Site.query.filter_by(code=code).first()

    @staticmethod
    def delete(site):
        db.session.delete(site)