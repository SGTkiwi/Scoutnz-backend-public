from marshmallow import Schema, fields


class JobPostUpdateSchema(Schema):
    job_post_title = fields.Str()
    job_post_category = fields.Str()
    hourly_wage = fields.Float()
    desired_education = fields.Str(allow_none=True)
    desired_age = fields.Int(allow_none=True)
    desired_gender = fields.Str(allow_none=True)
    working_days = fields.Str()
    working_hours = fields.Float()
    working_period = fields.Int(allow_none=True)
    job_description = fields.Str()
