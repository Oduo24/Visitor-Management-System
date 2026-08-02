from werkzeug.security import generate_password_hash

from app.models.user import User


class UserSeeder:

    @staticmethod
    def run(
        organization,
        department,
    ):

        user = User.query.filter_by(
            email="admin@test.com"
        ).first()

        if user:
            return user

        user = User(
            organization=organization,
            department=department,
            first_name="System",
            last_name="Administrator",
            email="admin@test.com",
            employee_number="EMP001",
            password_hash=generate_password_hash(
                "Password123!"
            ),
            is_active=True,
        )

        return user