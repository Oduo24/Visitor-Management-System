from marshmallow import (
    Schema,
    fields,
)
 
 
class VisitAccessPassResponseSchema(Schema):
 
    visit_id = fields.UUID()
 
    visitor_name = fields.String()
 
    company = fields.String(
        allow_none=True
    )
 
    vehicle_registration = (
        fields.String(
            allow_none=True
        )
    )
 
    visitor_code = fields.String()
 
    host = fields.String()
 
    site = fields.String()
 
    destination = fields.String(
        allow_none=True
    )
 
    visit_type = fields.String()
 
    status = fields.String()
 
    purpose = fields.String(
        allow_none=True
    )
 
    expected_arrival = (
        fields.DateTime(
            allow_none=True
        )
    )
 
    expected_departure = (
        fields.DateTime(
            allow_none=True
        )
    )
 
    qr_token = fields.String()
 
    pass_generated_at = (
        fields.DateTime(
            allow_none=True
        )
    )