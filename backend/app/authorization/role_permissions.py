from app.authorization.permissions import Permission


ROLE_PERMISSIONS = {

    "SUPER_ADMIN": {
        "*",
    },

    "ORG_ADMIN": {
        Permission.VISITOR_CREATE,
        Permission.VISITOR_READ,
        Permission.VISITOR_UPDATE,
        Permission.VISITOR_DELETE,

        Permission.VISIT_CREATE,
        Permission.VISIT_READ,
        Permission.VISIT_UPDATE,
        Permission.VISIT_APPROVE,
        Permission.VISIT_CHECKIN,
        Permission.VISIT_CHECKOUT,

        Permission.HOST_CREATE,
        Permission.HOST_READ,
        Permission.HOST_UPDATE,
        Permission.HOST_DELETE,

        Permission.USER_CREATE,
        Permission.USER_READ,
        Permission.USER_UPDATE,
        Permission.USER_DELETE,

        Permission.REPORT_VIEW,
    },

    "SITE_ADMIN": {
        Permission.VISITOR_CREATE,
        Permission.VISITOR_READ,
        Permission.VISITOR_UPDATE,

        Permission.VISIT_CREATE,
        Permission.VISIT_READ,
        Permission.VISIT_CHECKIN,
        Permission.VISIT_CHECKOUT,

        Permission.REPORT_VIEW,
    },

    "RECEPTIONIST": {
        Permission.VISITOR_CREATE,
        Permission.VISITOR_READ,

        Permission.VISIT_CREATE,
        Permission.VISIT_READ,
        Permission.VISIT_CHECKIN,
    },

    "SECURITY_OFFICER": {
        Permission.VISIT_READ,
        Permission.VISIT_CHECKIN,
        Permission.VISIT_CHECKOUT,
    },

    "HOST": {
        Permission.VISIT_CREATE,
        Permission.VISIT_READ,
    },
}