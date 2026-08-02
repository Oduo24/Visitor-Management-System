from marshmallow import Schema, fields, validate


class RoleCreateSchema(Schema):
    organization_id = fields.UUID(required=True)

    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100),
    )

    code = fields.String(
        required=True,
        validate=validate.Length(min=2, max=30),
    )

    description = fields.String()

    is_active = fields.Boolean()


class RoleUpdateSchema(Schema):
    organization_id = fields.UUID()

    name = fields.String(
        validate=validate.Length(min=2, max=100),
    )

    code = fields.String(
        validate=validate.Length(min=2, max=30),
    )

    description = fields.String()

    is_active = fields.Boolean()


class RoleResponseSchema(Schema):
    id = fields.UUID()
    organization_id = fields.UUID()
    name = fields.String()
    code = fields.String()
    description = fields.String()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()