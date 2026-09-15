from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
)
 
 
class VisitDashboardQuerySchema(Schema):
 
    status = fields.String(
        load_default=None
    )
 
    site_id = fields.String(
        load_default=None
    )
 
    visit_type = fields.String(
        load_default=None
    )
 
    start_date = fields.Date(
        load_default=None
    )
 
    end_date = fields.Date(
        load_default=None
    )
 
 
    @validates_schema
    def validate_date_range(
        self,
        data,
        **kwargs,
    ):
        start_date = data.get(
            "start_date"
        )
 
        end_date = data.get(
            "end_date"
        )
 
        if (
            start_date
            and end_date
            and start_date > end_date
        ):
            raise ValidationError(
                "start_date cannot be "
                "after end_date."
            )

class VisitDashboardResponseSchema(
    Schema
):
 
    total_visits = fields.Integer()
 
    pending_approval = fields.Integer()
 
    approved = fields.Integer()
 
    checked_in = fields.Integer()
 
    checked_out = fields.Integer()
 
    status_breakdown = fields.Dict(
        keys=fields.String(),
        values=fields.Integer(),
    )
 
    visit_type_breakdown = fields.Dict(
        keys=fields.String(),
        values=fields.Integer(),
    )