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

from marshmallow import (
    Schema,
    fields,
)


class VisitResponseSchema(Schema):

    id = fields.UUID()

    visitor_id = fields.UUID()
    host_id = fields.UUID()
    destination_id = fields.UUID()
    site_id = fields.UUID()

    visitor_name = fields.Method(
        "get_visitor_name"
    )

    host_name = fields.Method(
        "get_host_name"
    )

    site_name = fields.Method(
        "get_site_name"
    )

    destination_name = fields.Method(
        "get_destination_name"
    )

    visit_type = fields.String()
    status = fields.String()

    purpose = fields.String(
        allow_none=True
    )

    expected_arrival = fields.DateTime(
        allow_none=True
    )

    expected_departure = fields.DateTime(
        allow_none=True
    )

    checked_in_at = fields.DateTime(
        allow_none=True
    )

    checked_out_at = fields.DateTime(
        allow_none=True
    )

    approved_by = fields.UUID(
        allow_none=True
    )

    approved_at = fields.DateTime(
        allow_none=True
    )

    rejected_by = fields.UUID(
        allow_none=True
    )
    rejected_at = fields.DateTime(
        allow_none=True
    )

    badge_number = fields.String(
        allow_none=True
    )

    visitor_code = fields.String(
        allow_none=True
    )

    visitor_code_generated_at = (
        fields.DateTime(
            allow_none=True
        )
    )

    qr_token = fields.String(
        allow_none=True
    )

    qr_generated_at = fields.DateTime(
        allow_none=True
    )

    notes = fields.String(
        allow_none=True
    )

    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    def get_visitor_name(
        self,
        visit,
    ):

        if not visit.visitor:
            return None

        return visit.visitor.full_name

    def get_host_name(
        self,
        visit,
    ):

        if not visit.host:
            return None

        return " ".join(
            part
            for part in (
                visit.host.first_name,
                visit.host.last_name,
            )
            if part
        )

    def get_site_name(
        self,
        visit,
    ):

        if not visit.site:
            return None

        return visit.site.name

    def get_destination_name(
        self,
        visit,
    ):

        if not visit.destination:
            return None

        return visit.destination.name