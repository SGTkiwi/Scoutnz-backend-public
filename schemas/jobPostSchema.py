from marshmallow import Schema, fields


class JobPostSchema(Schema):
    job_post_id = fields.Int(dump_only=True)
    business_profile_id = fields.Int(dump_only=True, load_only=True)
    job_post_title = fields.Str(required=True)
    job_post_category = fields.Str(required=True)
    hourly_wage = fields.Float(required=True)
    desired_education = fields.Str(allow_none=True)
    desired_age = fields.Int(allow_none=True)
    desired_gender = fields.Str(allow_none=True)
    working_days = fields.Str(required=True)
    working_hours = fields.Float(required=True)
    working_period = fields.Int(allow_none=True)
    job_description = fields.Str(required=True)
    date_posted = fields.Date(dump_only=True)
