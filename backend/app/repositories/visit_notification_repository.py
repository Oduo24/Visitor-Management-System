from app.extensions import db

from app.models.visit_notification import (
    VisitNotification,
)


class VisitNotificationRepository:

    @staticmethod
    def create(notification):

        db.session.add(notification)

        return notification

    @staticmethod
    def get_by_id(notification_id):

        return db.session.get(
            VisitNotification,
            notification_id,
        )

    @staticmethod
    def get_by_visit_id(visit_id):

        return (
            VisitNotification.query
            .filter(
                VisitNotification.visit_id
                == visit_id
            )
            .order_by(
                VisitNotification.created_at.desc()
            )
            .all()
        )