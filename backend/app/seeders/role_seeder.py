from app.models.role import Role


class RoleSeeder:

    @staticmethod
    def run(organization):

        role = Role.query.filter_by(
            code="SUPER_ADMIN"
        ).first()

        if role:
            return role

        role = Role(
            organization=organization,
            name="System Administrator",
            code="SUPER_ADMIN",
            description="System Administrator",
        )

        return role