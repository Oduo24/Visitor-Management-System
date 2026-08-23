from app.models.visitor import Visitor
 
 
class VisitorSeeder:
 
    @staticmethod
    def run():
 
        visitor = Visitor.query.filter_by(
            email="john.kamau@example.com"
        ).first()
 
        if visitor:
            return visitor
 
        visitor = Visitor(
            first_name="John",
            middle_name=None,
            last_name="Kamau",
            gender="MALE",
            email="john.kamau@example.com",
            phone="+254700000001",
            company="Demo Company Ltd",
            nationality="Kenyan",
            id_number="12345678",
            passport_number=None,
            vehicle_registration="KAA123A",
            is_blacklisted=False,
            notes="Seeded visitor",
        )
 
        return visitor