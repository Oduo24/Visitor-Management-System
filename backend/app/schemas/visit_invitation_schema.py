from marshmallow import Schema, fields


class VisitInvitationVisitorSchema(Schema):
    # describes what the frontend receives.

    first_name = fields.String(
        required=True
    )

    middle_name = fields.String(
        allow_none=True
    )

    last_name = fields.String(
        required=True
    )

    phone = fields.String(
        required=True
    )

    email = fields.Email(
        allow_none=True
    )

    id_number = fields.String(
        allow_none=True
    )

    passport_number = fields.String(
        allow_none=True
    )

    vehicle_registration = fields.String(
        allow_none=True
    )


class VisitInvitationUpdateSchema(Schema):
    # describes what the visitor is allowed to submit.

    first_name = fields.String()

    middle_name = fields.String(
        allow_none=True
    )

    last_name = fields.String()

    phone = fields.String()

    email = fields.Email(
        allow_none=True
    )

    id_number = fields.String(
        allow_none=True
    )

    passport_number = fields.String(
        allow_none=True
    )

    vehicle_registration = fields.String(
        allow_none=True
    )


class VisitInvitationResponseSchema(Schema):
    # describes the public GET response.

    visit_id = fields.UUID()

    site = fields.String()

    host = fields.String()

    visit_type = fields.String()

    expected_arrival = fields.DateTime(
        allow_none=True
    )

    purpose = fields.String(
        allow_none=True
    )

    visitor = fields.Nested(
        VisitInvitationVisitorSchema
    )

    expires_at = fields.DateTime()