from app.models.user_site_role import UserSiteRole


class UserSiteRoleSeeder:

    @staticmethod
    def run(user, site, role):

        assignment = UserSiteRole.query.filter_by(
            user_id=user.id,
            site_id=site.id,
            role_id=role.id,
        ).first()

        if assignment:
            return assignment

        return UserSiteRole(
            user=user,
            site=site,
            role=role,
        )