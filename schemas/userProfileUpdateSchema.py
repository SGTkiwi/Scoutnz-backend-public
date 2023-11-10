from marshmallow import Schema, fields


class UserProfileUpdateSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    phone_number = fields.Str()
    user_photo = fields.Raw(allow_none=True)
    nationality = fields.Str(allow_none=True)
