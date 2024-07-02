from marshmallow import Schema, fields

class UserInfoSchema(Schema):
    id = fields.Int(dump_only=True)
    userno = fields.Str(required=True)
    username = fields.Str(required=True)
    password_hash = fields.Str(load_only=True)
    email = fields.Email(required=True)