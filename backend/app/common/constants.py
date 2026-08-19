class VisitStatus:
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"

class VisitType:
    PREBOOKED = "PREBOOKED"
    WALK_IN = "WALK_IN"

class Roles:
    ADMIN = "Admin"
    RECEPTIONIST = "Receptionist"
    SECURITY = "Security Officer"
    HOST = "Host"

class VisitAuditAction:

    CREATED = "CREATED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    BADGE_ISSUED = "BADGE_ISSUED"
    QR_GENERATED = "QR_GENERATED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"

class NotificationChannel:
    EMAIL = "EMAIL"
    SMS = "SMS"
    IN_APP = "IN_APP"


class NotificationStatus:
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"


class VisitNotificationEvent:
    CREATED = "VISIT_CREATED"
    INVITED = "VISITOR_INVITED"
    APPROVED = "VISIT_APPROVED"
    REJECTED = "VISIT_REJECTED"
    CHECKED_IN = "VISITOR_CHECKED_IN"
    CHECKED_OUT = "VISITOR_CHECKED_OUT"

class VisitInvitationStatus:
    ACTIVE = "ACTIVE"
    USED = "USED"
    EXPIRED = "EXPIRED"