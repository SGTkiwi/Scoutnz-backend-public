from marshmallow import Schema, fields


class BusinessProfileUpdateSchema(Schema):
    business_name = fields.Str()
    business_address = fields.Str()
    billing_address = fields.Str(allow_none=True)
    business_number = fields.Str()
    business_logo = fields.Raw(allow_none=True)
    business_info = fields.Str(allow_none=True)
