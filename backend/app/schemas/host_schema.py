from marshmallow import Schema, fields



class HostResponseSchema(Schema):

    id = fields.UUID()
    organization_id = fields.UUID()
    department_id = fields.UUID()

    first_name = fields.String()
    last_name = fields.String()

    email = fields.Email()

    phone = fields.String()

    employee_number = fields.String()

    job_title = fields.String()