from app.common.database import DatabaseSession
from app.extensions import db
from app.common.database import DatabaseSession
from app.seeders.organization_seeder import OrganizationSeeder
from app.seeders.department_seeder import DepartmentSeeder
from app.seeders.site_seeder import SiteSeeder
from app.seeders.role_seeder import RoleSeeder
from app.seeders.user_seeder import UserSeeder
from app.seeders.user_site_role_seeder import UserSiteRoleSeeder


class DatabaseSeeder:

    @staticmethod
    def run():

        organization = OrganizationSeeder.run()
        db.session.add(organization)
        DatabaseSession.commit()

        department = DepartmentSeeder.run(organization)
        site = SiteSeeder.run(organization)
        role = RoleSeeder.run(organization)
        user = UserSeeder.run(
            organization,
            department,
        )

        db.session.add_all([
            department,
            site,
            role,
            user,
        ])

        DatabaseSession.commit()

        assignment = UserSiteRoleSeeder.run(
            user,
            site,
            role,
        )

        db.session.add(assignment)
        DatabaseSession.commit()

        return {
            "organization": organization,
            "department": department,
            "site": site,
            "role": role,
            "user": user,
            "assignment": assignment,
        }