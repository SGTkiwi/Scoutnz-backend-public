from marshmallow import Schema, fields


class BusinessProfileSchema(Schema):
    business_profile_id = fields.Int(dump_only=True, load_only=True)
    account_id = fields.Int(dump_only=True, load_only=True)
    business_name = fields.Str(required=True)
    business_address = fields.Str(required=True)
    billing_address = fields.Str(allow_none=True)
    nzbn = fields.Str(allow_none=True)
    business_number = fields.Str(required=True)
    business_logo = fields.Raw(allow_none=True)
    business_info = fields.Str(allow_none=True)
