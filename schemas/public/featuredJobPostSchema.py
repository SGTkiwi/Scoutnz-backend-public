from marshmallow import Schema, fields
from schemas import ExtendedJobPostSchema

class FeaturedJobPostSchema(Schema):
    post_premium_id = fields.Integer(dump_only=True)
    job_post = fields.Nested(ExtendedJobPostSchema(), dump_only=True)
    


    

