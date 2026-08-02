from app.models.site import Site


class SiteSeeder:

    @staticmethod
    def run(organization):

        site = Site.query.filter_by(
            code="HQ"
        ).first()

        if site:
            return site

        site = Site(
            organization=organization,
            name="Head Office",
            code="HQ",
            city="Nairobi",
            country="Kenya",
            is_active=True,
        )

        return site