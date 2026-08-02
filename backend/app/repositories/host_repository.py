from app.models.user import User


class HostRepository:

    @staticmethod
    def get_all():

        return (
            User.query
            .filter_by(is_active=True)
            .order_by(
                User.first_name,
                User.last_name,
            )
            .all()
        )

    @staticmethod
    def get_by_id(host_id):

        return User.query.get(host_id)

    @staticmethod
    def search(query):

        return (
            User.query
            .filter(
                User.is_active == True,
                (
                    User.first_name.ilike(f"%{query}%")
                    | User.last_name.ilike(f"%{query}%")
                    | User.email.ilike(f"%{query}%")
                    | User.employee_number.ilike(f"%{query}%")
                ),
            )
            .all()
        )