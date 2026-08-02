from marshmallow import Schema, fields, validate


class DestinationCreateSchema(Schema):
    floor_id = fields.UUID(required=True)
    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=150),
    )
    code = fields.String(
        validate=validate.Length(max=30)
    )
    is_active = fields.Boolean()


class DestinationUpdateSchema(Schema):
    floor_id = fields.UUID()
    name = fields.String(
        validate=validate.Length(min=2, max=150),
    )
    code = fields.String(
        validate=validate.Length(max=30)
    )
    is_active = fields.Boolean()


class DestinationResponseSchema(Schema):
    id = fields.UUID()
    floor_id = fields.UUID()
    name = fields.String()
    code = fields.String()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()