from app.extensions import db
from app.models.organization import Organization


class OrganizationRepository:

    @staticmethod
    def create(organization):
        """Add a new organization to the current session."""
        db.session.add(organization)
        return organization

    @staticmethod
    def get_all():
        """Return all organizations ordered by name."""
        return (
            Organization.query
            .order_by(Organization.name.asc())
            .all()
        )

    @staticmethod
    def get_by_id(organization_id):
        """Return an organization by its ID."""
        return db.session.get(Organization, organization_id)

    @staticmethod
    def get_by_code(code):
        """Return an organization by its unique code."""
        return (
            Organization.query
            .filter_by(code=code)
            .first()
        )

    @staticmethod
    def delete(organization):
        """Mark an organization for deletion."""
        db.session.delete(organization)