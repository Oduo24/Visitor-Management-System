from marshmallow import Schema, fields, validate


class VisitCreateSchema(Schema):

    visitor_id = fields.UUID(required=True)

    host_id = fields.UUID(required=True)

    destination_id = fields.UUID(required=True)

    site_id = fields.UUID(required=True)

    visit_type = fields.String(required=True)

    purpose = fields.String()

    expected_arrival = fields.DateTime()

    expected_departure = fields.DateTime()

    notes = fields.String()

class VisitUpdateSchema(Schema):

    host_id = fields.UUID()

    destination_id = fields.UUID()

    purpose = fields.String()

    expected_arrival = fields.DateTime()

    expected_departure = fields.DateTime()

    notes = fields.String()

class VisitResponseSchema(Schema):

    id = fields.UUID()
    visitor_id = fields.UUID()
    host_id = fields.UUID()
    destination_id = fields.UUID()
    site_id = fields.UUID()
    visit_type = fields.String()
    status = fields.String()
    purpose = fields.String()
    expected_arrival = fields.DateTime()
    expected_departure = fields.DateTime()
    checked_in_at = fields.DateTime()
    checked_out_at = fields.DateTime()
    approved_by = fields.UUID()
    approved_at = fields.DateTime()
    badge_number = fields.String()
    notes = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    qr_token = fields.String()
    qr_generated_at = fields.DateTime()
    visitor_code = fields.String()
    visitor_code_generated_at = fields.DateTime()