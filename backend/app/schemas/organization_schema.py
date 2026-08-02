from marshmallow import fields, validate

from app.schemas.base_schema import BaseSchema


class OrganizationCreateSchema(BaseSchema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=150)
    )

    code = fields.String(
        required=True,
        validate=validate.Length(min=2, max=20)
    )

    email = fields.Email(load_default=None)
    phone = fields.String(load_default=None)
    website = fields.String(load_default=None)
    logo_url = fields.String(load_default=None)
    description = fields.String(load_default=None)


class OrganizationResponseSchema(BaseSchema):
    id = fields.String()
    name = fields.String()
    code = fields.String()
    email = fields.String()
    phone = fields.String()
    website = fields.String()
    logo_url = fields.String()
    description = fields.String()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class OrganizationUpdateSchema(BaseSchema):
    name = fields.String()
    code = fields.String()
    email = fields.Email()
    phone = fields.String()
    website = fields.String()
    logo_url = fields.String()
    description = fields.String()
    is_active = fields.Boolean()