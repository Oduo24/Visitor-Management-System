from marshmallow import Schema, fields, validate


class DepartmentCreateSchema(Schema):
    organization_id = fields.UUID(required=True)

    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=150),
    )

    code = fields.String(
        required=True,
        validate=validate.Length(min=2, max=30),
    )

    description = fields.String()

    is_active = fields.Boolean()


class DepartmentUpdateSchema(Schema):
    organization_id = fields.UUID()

    name = fields.String(
        validate=validate.Length(min=2, max=150),
    )

    code = fields.String(
        validate=validate.Length(min=2, max=30),
    )

    description = fields.String()

    is_active = fields.Boolean()


class DepartmentResponseSchema(Schema):
    id = fields.UUID()
    organization_id = fields.UUID()
    name = fields.String()
    code = fields.String()
    description = fields.String()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()