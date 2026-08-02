from marshmallow import Schema, fields, validate


class VisitorCreateSchema(Schema):

    first_name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )

    middle_name = fields.String(
        validate=validate.Length(max=100),
        allow_none=True,
    )

    last_name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )

    gender = fields.String(
        validate=validate.OneOf(
            ["Male", "Female", "Other"]
        ),
        allow_none=True,
    )

    date_of_birth = fields.Date(
        allow_none=True,
    )

    phone = fields.String(
        required=True,
        validate=validate.Length(max=30),
    )

    email = fields.Email(
        allow_none=True,
    )

    company = fields.String(
        validate=validate.Length(max=255),
        allow_none=True,
    )

    address = fields.String(
        validate=validate.Length(max=255),
        allow_none=True,
    )

    nationality = fields.String(
        validate=validate.Length(max=100),
        allow_none=True,
    )

    id_number = fields.String(
        validate=validate.Length(max=100),
        allow_none=True,
    )

    passport_number = fields.String(
        validate=validate.Length(max=100),
        allow_none=True,
    )

    vehicle_registration = fields.String(
        validate=validate.Length(max=50),
        allow_none=True,
    )

    photo_url = fields.String(
        allow_none=True,
    )

    is_blacklisted = fields.Boolean()

    notes = fields.String(
        allow_none=True,
    )


class VisitorUpdateSchema(Schema):

    first_name = fields.String(
        validate=validate.Length(min=1, max=100),
    )

    middle_name = fields.String(
        validate=validate.Length(max=100),
        allow_none=True,
    )

    last_name = fields.String(
        validate=validate.Length(min=1, max=100),
    )

    gender = fields.String(
        validate=validate.OneOf(
            ["Male", "Female", "Other"]
        ),
        allow_none=True,
    )

    date_of_birth = fields.Date(
        allow_none=True,
    )

    phone = fields.String(
        validate=validate.Length(max=30),
    )

    email = fields.Email(
        allow_none=True,
    )

    company = fields.String(
        validate=validate.Length(max=255),
        allow_none=True,
    )

    address = fields.String(
        validate=validate.Length(max=255),
        allow_none=True,
    )

    nationality = fields.String(
        validate=validate.Length(max=100),
        allow_none=True,
    )

    id_number = fields.String(
        validate=validate.Length(max=100),
        allow_none=True,
    )

    passport_number = fields.String(
        validate=validate.Length(max=100),
        allow_none=True,
    )

    vehicle_registration = fields.String(
        validate=validate.Length(max=50),
        allow_none=True,
    )

    photo_url = fields.String(
        allow_none=True,
    )

    is_blacklisted = fields.Boolean()

    notes = fields.String(
        allow_none=True,
    )


class VisitorResponseSchema(Schema):

    id = fields.UUID()

    first_name = fields.String()
    middle_name = fields.String()
    last_name = fields.String()

    gender = fields.String()
    date_of_birth = fields.Date()

    email = fields.Email()
    phone = fields.String()

    company = fields.String()
    address = fields.String()

    nationality = fields.String()

    id_number = fields.String()
    passport_number = fields.String()

    vehicle_registration = fields.String()

    photo_url = fields.String()

    is_blacklisted = fields.Boolean()

    notes = fields.String()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()