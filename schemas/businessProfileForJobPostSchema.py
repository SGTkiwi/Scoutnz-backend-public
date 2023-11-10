from marshmallow import Schema, fields


class BusinessProfileForJobPostSchema(Schema):
    business_name = fields.Str(required=True)
    business_address = fields.Str(required=True)
    business_number = fields.Str(required=True)
    business_logo = fields.Raw(allow_none=True)
