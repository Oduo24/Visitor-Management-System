from marshmallow import Schema, fields, validate


class FloorCreateSchema(Schema):
    building_id = fields.UUID(required=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    level = fields.Integer(required=True)
    is_active = fields.Boolean()


class FloorUpdateSchema(Schema):
    building_id = fields.UUID()
    name = fields.String(validate=validate.Length(min=1, max=100))
    level = fields.Integer()
    is_active = fields.Boolean()


class FloorResponseSchema(Schema):
    id = fields.UUID()
    building_id = fields.UUID()
    name = fields.String()
    level = fields.Integer()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()