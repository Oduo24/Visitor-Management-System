from marshmallow import Schema, fields


class UserSiteRoleCreateSchema(Schema):
    user_id = fields.UUID(required=True)
    site_id = fields.UUID(required=True)
    role_id = fields.UUID(required=True)


class UserSiteRoleResponseSchema(Schema):
    id = fields.UUID()

    user_id = fields.UUID()
    site_id = fields.UUID()
    role_id = fields.UUID()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()