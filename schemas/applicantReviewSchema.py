from marshmallow import Schema, fields

    
class ApplicantReviewSchema(Schema):
    application_id = fields.Int(required=True)
    cv_id = fields.Int(required=True)
    job_post_id = fields.Int(required=True)
    date_applied = fields.Date(dump_only=True)
    status = fields.Str(required=True)
    