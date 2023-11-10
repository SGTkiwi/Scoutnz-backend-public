from marshmallow import Schema, fields


class UserMembershipSchema(Schema):
    user_membership_id = fields.Int(dump_only=True)
    user_profile_id = fields.Int(dump_only=True)
    user_membership_tier = fields.Str(required=True)
    date_purchased = fields.Date(required=True)
    user_membership_end_date = fields.Date(required=True)

