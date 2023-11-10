from marshmallow import Schema, fields


class ApplicationSchema(Schema):
    application_id = fields.Int(dump_only=True, load_only=True)
    cv_id = fields.Int(allow_none=True)
    job_post_id = fields.Int(allow_none=True)
    date_applied = fields.Date(dump_only=True)
    status = fields.Str(dump_only=True)
    