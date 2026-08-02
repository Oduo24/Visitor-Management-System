from marshmallow import Schema, fields, validate


class SiteCreateSchema(Schema):
    organization_id = fields.UUID(required=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=150))
    code = fields.String(required=True, validate=validate.Length(min=2, max=30))
    address = fields.String()
    city = fields.String()
    country = fields.String()
    phone = fields.String()
    email = fields.Email()
    is_active = fields.Boolean()


class SiteUpdateSchema(Schema):
    organization_id = fields.UUID()
    name = fields.String(validate=validate.Length(min=2, max=150))
    code = fields.String(validate=validate.Length(min=2, max=30))
    address = fields.String()
    city = fields.String()
    country = fields.String()
    phone = fields.String()
    email = fields.Email()
    is_active = fields.Boolean()


class SiteResponseSchema(Schema):
    id = fields.UUID()
    organization_id = fields.UUID()
    name = fields.String()
    code = fields.String()
    address = fields.String()
    city = fields.String()
    country = fields.String()
    phone = fields.String()
    email = fields.Email()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()