from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    organization_id = fields.UUID(required=True)
    department_id = fields.UUID(allow_none=True)

    first_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100),
    )

    last_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100),
    )

    email = fields.Email(required=True)

    phone = fields.String()

    employee_number = fields.String(
        validate=validate.Length(max=50)
    )

    job_title = fields.String(
        validate=validate.Length(max=150)
    )

    profile_photo_url = fields.Url()

    password = fields.String(
        required=True,
        validate=validate.Length(min=8),
        load_only=True,
    )

    is_active = fields.Boolean()


class UserUpdateSchema(Schema):
    organization_id = fields.UUID()
    department_id = fields.UUID(allow_none=True)

    first_name = fields.String(
        validate=validate.Length(min=2, max=100),
    )

    last_name = fields.String(
        validate=validate.Length(min=2, max=100),
    )

    email = fields.Email()

    phone = fields.String()

    employee_number = fields.String(
        validate=validate.Length(max=50)
    )

    job_title = fields.String(
        validate=validate.Length(max=150)
    )

    profile_photo_url = fields.Url()

    password = fields.String(
        validate=validate.Length(min=8),
        load_only=True,
    )

    is_active = fields.Boolean()


class UserResponseSchema(Schema):
    id = fields.UUID()
    organization_id = fields.UUID()
    department_id = fields.UUID(allow_none=True)

    first_name = fields.String()
    last_name = fields.String()
    full_name = fields.String()

    email = fields.Email()
    phone = fields.String()

    employee_number = fields.String()

    job_title = fields.String()

    profile_photo_url = fields.String()

    last_login_at = fields.DateTime(
        allow_none=True
    )

    is_active = fields.Boolean()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()