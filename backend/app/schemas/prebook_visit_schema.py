from marshmallow import Schema, fields


class PrebookVisitCreateSchema(Schema):

    visitor_id = fields.UUID(required=True)

    host_id = fields.UUID(required=True)

    destination_id = fields.UUID(required=True)

    site_id = fields.UUID(required=True)

    expected_arrival = fields.DateTime(required=True)

    expected_departure = fields.DateTime(
        allow_none=True,
    )

    purpose = fields.String(required=True)

    notes = fields.String(
        allow_none=True,
    )