from marshmallow import Schema, fields


class VisitApprovalSchema(Schema):

    approved = fields.Boolean(
        required=True
    )

    notes = fields.String(
        required=False
    )

    approved_at = fields.DateTime(dump_only=True)
    approved_by = fields.String(dump_only=True)