from marshmallow import Schema, fields
from schemas import AccountSchema


class BusinessSignUpSchema(AccountSchema):
    business_profile_id = fields.Int(dump_only=True)
    business_name = fields.Str(required=True)
    business_address = fields.Str(required=True)
    business_number = fields.Str(required=True)
