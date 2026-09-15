from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
)
 
 
class VisitActivityReportQuerySchema(
    Schema
):
 
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
    def validate_dates(
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