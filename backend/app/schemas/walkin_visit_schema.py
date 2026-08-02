from marshmallow import Schema, fields


class WalkinVisitCreateSchema(Schema):

    visitor_id = fields.UUID(required=True)

    host_id = fields.UUID(required=True)

    destination_id = fields.UUID(required=True)

    site_id = fields.UUID(required=True)

    purpose = fields.String(required=False)

    notes = fields.String(required=False)