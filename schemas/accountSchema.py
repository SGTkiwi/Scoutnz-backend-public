from marshmallow import Schema, fields, validate


class AccountSchema(Schema):
    account_id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=8)
    )
    account_type = fields.Int()
    date_created = fields.Date(dump_only=True)
