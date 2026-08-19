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