from marshmallow import Schema, fields
from schemas import AccountSchema

class UserSignUpSchema(AccountSchema):
    user_profile_id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(required=True, unique=True)
    date_of_birth = fields.Date(required=True)
    gender = fields.Str(required=True)

