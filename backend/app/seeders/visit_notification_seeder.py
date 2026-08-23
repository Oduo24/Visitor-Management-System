from datetime import (
    datetime,
    timezone,
)
 
from app.common.constants import (
    NotificationChannel,
    NotificationStatus,
    VisitNotificationEvent,
)
 
from app.models.visit_notification import (
    VisitNotification,
)
 
 
class VisitNotificationSeeder:
 
    @staticmethod
    def run(
        visit,
        visitor,
    ):
 
        recipient = visitor.email
 
        notification = (
            VisitNotification.query
            .filter_by(
                visit_id=visit.id,
                recipient=recipient,
                channel=(
                    NotificationChannel.EMAIL
                ),
                event=(
                    VisitNotificationEvent
                    .VISITOR_INVITED
                ),
            )
            .first()
        )
 
        if notification:
            return notification
 
        now = datetime.now(
            timezone.utc
        ).replace(
            tzinfo=None
        )
 
        notification = (
            VisitNotification(
                visit_id=visit.id,
 
                recipient=recipient,
 
                channel=(
                    NotificationChannel.EMAIL
                ),
 
                event=(
                    VisitNotificationEvent
                    .VISITOR_INVITED
                ),
 
                status=(
                    NotificationStatus.SENT
                ),
 
                subject=(
                    "Visitor Invitation"
                ),
 
                message=(
                    "Your seeded visit "
                    "invitation has been created."
                ),
 
                provider_message_id=(
                    "seed-notification"
                ),
 
                sent_at=now,
 
                error_message=None,
            )
        )
 
        return notification