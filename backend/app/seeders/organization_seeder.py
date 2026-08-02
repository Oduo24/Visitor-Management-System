from app.models.organization import Organization


class OrganizationSeeder:

    @staticmethod
    def run():

        organization = Organization.query.filter_by(
            code="ACME"
        ).first()

        if organization:
            return organization

        organization = Organization(
            name="Acme Ltd",
            code="ACME",
            email="info@acme.test",
            phone="+254700000000",
            is_active=True,
        )

        return organization