from app.models.department import Department


class DepartmentSeeder:

    @staticmethod
    def run(organization):

        department = Department.query.filter_by(
            code="ICT"
        ).first()

        if department:
            return department

        department = Department(
            organization=organization,
            name="ICT",
            code="ICT",
            is_active=True,
        )

        return department