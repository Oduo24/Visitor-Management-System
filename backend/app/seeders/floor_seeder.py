from app.models.floor import Floor
 
 
class FloorSeeder:
 
    @staticmethod
    def run(building):
 
        floor = Floor.query.filter_by(
            building_id=building.id,
            level=0,
        ).first()
 
        if floor:
            return floor
 
        floor = Floor(
            building=building,
            name="Ground Floor",
            level=0,
            is_active=True,
        )
 
        return floor