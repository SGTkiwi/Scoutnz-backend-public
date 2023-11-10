from marshmallow import Schema, fields
from schemas import JobPostSchema, BusinessProfileForJobPostSchema


class ExtendedJobPostSchema(JobPostSchema):
    business_profile = fields.Nested(BusinessProfileForJobPostSchema(), dump_only=True)

