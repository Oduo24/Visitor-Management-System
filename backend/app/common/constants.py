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