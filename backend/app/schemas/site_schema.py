from marshmallow import (
    Schema,
    fields,
    validate,
)
 
 
class SiteCreateSchema(Schema):
 
    organization_id = fields.UUID(
        required=True
    )
 
    name = fields.String(
        required=True,
        validate=validate.Length(
            min=2,
            max=150,
        ),
    )
 
    code = fields.String(
        required=True,
        validate=validate.Length(
            min=2,
            max=20,
        ),
    )
 
    address = fields.String(
        allow_none=True
    )
 
    city = fields.String(
        allow_none=True
    )
 
    country = fields.String(
        allow_none=True
    )
 
    timezone = fields.String(
        validate=validate.Length(
            min=1,
            max=50,
        )
    )
 
    phone = fields.String(
        allow_none=True
    )
 
    email = fields.Email(
        allow_none=True
    )
 
    is_active = fields.Boolean()
 
 
class SiteUpdateSchema(Schema):
 
    organization_id = fields.UUID()
 
    name = fields.String(
        validate=validate.Length(
            min=2,
            max=150,
        )
    )
 
    code = fields.String(
        validate=validate.Length(
            min=2,
            max=20,
        )
    )
 
    address = fields.String(
        allow_none=True
    )
 
    city = fields.String(
        allow_none=True
    )
 
    country = fields.String(
        allow_none=True
    )
 
    timezone = fields.String(
        validate=validate.Length(
            min=1,
            max=50,
        )
    )
 
    phone = fields.String(
        allow_none=True
    )
 
    email = fields.Email(
        allow_none=True
    )
 
    is_active = fields.Boolean()
 
 
class SiteResponseSchema(Schema):
 
    id = fields.UUID()
 
    organization_id = fields.UUID()
 
    name = fields.String()
 
    code = fields.String()
 
    address = fields.String(
        allow_none=True
    )
 
    city = fields.String(
        allow_none=True
    )
 
    country = fields.String(
        allow_none=True
    )
 
    timezone = fields.String()
 
    phone = fields.String(
        allow_none=True
    )
 
    email = fields.Email(
        allow_none=True
    )
 
    is_active = fields.Boolean()
 
    created_at = fields.DateTime()
 
    updated_at = fields.DateTime()