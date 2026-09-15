from sqlalchemy import or_, func

from app.extensions import db
from app.models.visit import Visit
from app.models.visitor import Visitor


class VisitRepository:

    @staticmethod
    def create(visit):
        db.session.add(visit)
        return visit

    @staticmethod
    def get_all():
        return (
            Visit.query
            .order_by(Visit.created_at.desc())
            .all()
        )

    @staticmethod
    def get_by_id(visit_id):
        return db.session.get(
            Visit,
            visit_id,
        )

    @staticmethod
    def get_by_qr_token(token):
        return (
            Visit.query
            .filter(
                Visit.qr_token == token
            )
            .first()
        )

    @staticmethod
    def delete(visit):
        db.session.delete(visit)

    @staticmethod
    def search(search):

        query = (
            Visit.query
            .join(Visit.visitor)
        )

        if search:
            search = search.strip()

            query = query.filter(
                or_(
                    Visitor.first_name.ilike(
                        f"%{search}%"
                    ),
                    Visitor.middle_name.ilike(
                        f"%{search}%"
                    ),
                    Visitor.last_name.ilike(
                        f"%{search}%"
                    ),
                    Visitor.phone.ilike(
                        f"%{search}%"
                    ),
                    Visitor.email.ilike(
                        f"%{search}%"
                    ),
                    Visitor.id_number.ilike(
                        f"%{search}%"
                    ),
                    Visitor.passport_number.ilike(
                        f"%{search}%"
                    ),
                    Visitor.vehicle_registration.ilike(
                        f"%{search}%"
                    ),
                )
            )

        return (
            query
            .order_by(Visit.created_at.desc())
            .all()
        )

    @staticmethod
    def _dashboard_query(
        status=None,
        site_id=None,
        visit_type=None,
        start_date=None,
        end_date=None,
    ):
        query = Visit.query
    
        if status:
            query = query.filter(
                Visit.status == status
            )
    
        if site_id:
            query = query.filter(
                Visit.site_id == site_id
            )
    
        if visit_type:
            query = query.filter(
                Visit.visit_type == visit_type
            )
    
        if start_date:
            query = query.filter(
                Visit.created_at >= start_date
            )
    
        if end_date:
            # end_date is exclusive
            query = query.filter(
                Visit.created_at < end_date
            )
    
        return query
 
 
    @staticmethod
    def dashboard(
        status=None,
        site_id=None,
        visit_type=None,
        start_date=None,
        end_date=None,
    ):
        query = (
            VisitRepository
            ._dashboard_query(
                status=status,
                site_id=site_id,
                visit_type=visit_type,
                start_date=start_date,
                end_date=end_date,
            )
        )
    
        return (
            query
            .order_by(
                Visit.created_at.desc()
            )
            .all()
        )
    
    
    @staticmethod
    def dashboard_summary(
        status=None,
        site_id=None,
        visit_type=None,
        start_date=None,
        end_date=None,
    ):
        query = (
            VisitRepository
            ._dashboard_query(
                status=status,
                site_id=site_id,
                visit_type=visit_type,
                start_date=start_date,
                end_date=end_date,
            )
        )
    
        total_visits = (
            query
            .with_entities(
                func.count(Visit.id)
            )
            .scalar()
            or 0
        )
    
    
        status_rows = (
            query
            .with_entities(
                Visit.status,
                func.count(Visit.id),
            )
            .group_by(
                Visit.status
            )
            .all()
        )
    
    
        visit_type_rows = (
            query
            .with_entities(
                Visit.visit_type,
                func.count(Visit.id),
            )
            .group_by(
                Visit.visit_type
            )
            .all()
        )
    
    
        return {
            "total_visits":
                total_visits,
    
            "status_breakdown": {
                status: count
                for status, count
                in status_rows
            },
    
            "visit_type_breakdown": {
                visit_type: count
                for visit_type, count
                in visit_type_rows
            },
        }


    @staticmethod
    def get_by_visitor_code(code):
    
        return (
            Visit.query
            .filter(
                Visit.visitor_code == code
            )
            .first()
        )

    @staticmethod
    def get_by_access_pass_token(token):
        return Visit.query.filter_by(
            access_pass_token=token
        ).first()