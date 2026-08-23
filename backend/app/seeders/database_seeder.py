from app.extensions import db
from app.common.database import DatabaseSession

from app.seeders.organization_seeder import (
    OrganizationSeeder,
)
from app.seeders.department_seeder import (
    DepartmentSeeder,
)
from app.seeders.site_seeder import (
    SiteSeeder,
)
from app.seeders.building_seeder import (
    BuildingSeeder,
)
from app.seeders.floor_seeder import (
    FloorSeeder,
)
from app.seeders.destination_seeder import (
    DestinationSeeder,
)
from app.seeders.role_seeder import (
    RoleSeeder,
)
from app.seeders.user_seeder import (
    UserSeeder,
)
from app.seeders.user_site_role_seeder import (
    UserSiteRoleSeeder,
)
from app.seeders.visitor_seeder import (
    VisitorSeeder,
)
from app.seeders.visit_seeder import (
    VisitSeeder,
)
from app.seeders.visit_audit_seeder import (
    VisitAuditSeeder,
)
from app.seeders.visit_invitation_seeder import (
    VisitInvitationSeeder,
)
from app.seeders.visit_notification_seeder import (
    VisitNotificationSeeder,
)


class DatabaseSeeder:

    @staticmethod
    def run():

        try:
            #
            # Organization
            #
            organization = (
                OrganizationSeeder.run()
            )

            db.session.add(
                organization
            )

            DatabaseSession.flush()

            #
            # Organization-level data
            #
            department = (
                DepartmentSeeder.run(
                    organization
                )
            )

            site = (
                SiteSeeder.run(
                    organization
                )
            )

            role = (
                RoleSeeder.run(
                    organization
                )
            )

            db.session.add_all([
                department,
                site,
                role,
            ])

            DatabaseSession.flush()

            #
            # Site hierarchy
            #
            building = (
                BuildingSeeder.run(
                    site
                )
            )

            db.session.add(
                building
            )

            DatabaseSession.flush()

            floor = (
                FloorSeeder.run(
                    building
                )
            )

            db.session.add(
                floor
            )

            DatabaseSession.flush()

            destination = (
                DestinationSeeder.run(
                    floor
                )
            )

            db.session.add(
                destination
            )

            DatabaseSession.flush()

            #
            # User
            #
            user = (
                UserSeeder.run(
                    organization,
                    department,
                )
            )

            db.session.add(
                user
            )

            DatabaseSession.flush()

            #
            # User → Site → Role
            #
            assignment = (
                UserSiteRoleSeeder.run(
                    user,
                    site,
                    role,
                )
            )

            db.session.add(
                assignment
            )

            DatabaseSession.flush()

            #
            # Visitor
            #
            visitor = (
                VisitorSeeder.run()
            )

            db.session.add(
                visitor
            )

            DatabaseSession.flush()

            #
            # Visit
            #
            visit = (
                VisitSeeder.run(
                    visitor=visitor,
                    host=user,
                    destination=destination,
                    site=site,
                )
            )

            db.session.add(
                visit
            )

            DatabaseSession.flush()

            #
            # Visit Audit
            #
            audit = (
                VisitAuditSeeder.run(
                    visit=visit,
                    user=user,
                )
            )

            db.session.add(
                audit
            )

            DatabaseSession.flush()

            #
            # Visitor Invitation
            #
            invitation = (
                VisitInvitationSeeder.run(
                    visit=visit
                )
            )

            db.session.add(
                invitation
            )

            DatabaseSession.flush()

            #
            # Notification
            #
            notification = (
                VisitNotificationSeeder.run(
                    visit=visit,
                    visitor=visitor,
                )
            )

            db.session.add(
                notification
            )

            #
            # Commit entire seed
            #
            DatabaseSession.commit()

            return {
                "organization": organization,
                "department": department,
                "site": site,
                "building": building,
                "floor": floor,
                "destination": destination,
                "role": role,
                "user": user,
                "assignment": assignment,
                "visitor": visitor,
                "visit": visit,
                "audit": audit,
                "invitation": invitation,
                "notification": notification,
            }

        except Exception:
            DatabaseSession.rollback()
            raise