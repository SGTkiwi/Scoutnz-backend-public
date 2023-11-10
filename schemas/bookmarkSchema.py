from marshmallow import Schema, fields


class BookmarkSchema(Schema):
    account_id = fields.Int(dump_only=True)
    bookmark_id = fields.Int()
    job_post_id = fields.Int()
