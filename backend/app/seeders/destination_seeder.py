from app.models.destination import Destination
 
 
class DestinationSeeder:
 
    @staticmethod
    def run(floor):
 
        destination = (
            Destination.query
            .filter_by(
                floor_id=floor.id,
                code="RECEPTION",
            )
            .first()
        )
 
        if destination:
            return destination
 
        destination = Destination(
            floor=floor,
            name="Reception",
            code="RECEPTION",
            is_active=True,
        )
 
        return destination