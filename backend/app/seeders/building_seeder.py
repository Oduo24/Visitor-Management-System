from app.models.building import Building
 
 
class BuildingSeeder:
 
    @staticmethod
    def run(site):
 
        building = Building.query.filter_by(
            site_id=site.id,
            code="MAIN",
        ).first()
 
        if building:
            return building
 
        building = Building(
            site=site,
            name="Main Building",
            code="MAIN",
            is_active=True,
        )
 
        return building