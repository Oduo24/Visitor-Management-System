class VisitStatus:
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"

class VisitType:
    PREBOOKED = "PREBOOKED"
    WALKIN = "WALKIN"

class Roles:
    ADMIN = "Admin"
    RECEPTIONIST = "Receptionist"
    SECURITY = "Security Officer"
    HOST = "Host"