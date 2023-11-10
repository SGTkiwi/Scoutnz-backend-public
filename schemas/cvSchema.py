from marshmallow import Schema, fields


class CvSchema(Schema):
    cv_id = fields.Int()
    user_profile_id = fields.Int(dump_only=True)
    cv_title = fields.Str(required=True)
    work_experience = fields.Str(allow_none=True)
    education = fields.Str(allow_none=True)
    desired_city = fields.Str(allow_none=True)
    desired_suburb = fields.Str(allow_none=True)
    desired_working_days = fields.Int(allow_none=True)
    desired_working_hours = fields.Float(allow_none=True)
    desired_working_period = fields.Int(allow_none=True)
    date_posted_cv = fields.Date(dump_only=True)
    public_or_private = fields.Boolean(allow_none=True)  # 0 public 1 private only
