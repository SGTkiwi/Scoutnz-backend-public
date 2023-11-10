from marshmallow import Schema, fields


class UserProfileSchema(Schema):
    user_profile_id = fields.Int(dump_only=True)
    account_id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    date_of_birth = fields.Date(required=True)
    gender = fields.Str(required=True)
    user_photo = fields.Raw(allow_none=True)
    nationality = fields.Str(allow_none=True)
