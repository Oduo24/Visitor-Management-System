from marshmallow import Schema, fields


class VisitAuditResponseSchema(Schema):

    id = fields.UUID()

    visit_id = fields.UUID()

    user_id = fields.UUID(
        allow_none=True
    )

    action = fields.String()

    notes = fields.String(
        allow_none=True
    )

    created_at = fields.DateTime()