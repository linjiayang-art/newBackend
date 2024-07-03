from marshmallow import Schema, fields

class UserInfoSchema(Schema):
    id = fields.Int(dump_only=True)
    userno = fields.Str(required=True)
    username = fields.Str(required=True)
    password_hash = fields.Str(load_only=True)
    email = fields.Email(required=True)

class MenuSchema(Schema):
    id = fields.Int(dump_only=True)
    parent_id = fields.Int()
    menu_path = fields.Str()
    component = fields.Str()
    redirect_url = fields.Str()
    menu_name = fields.Str()
    menu_icon = fields.Str()
    menu_type = fields.Str()
    menu_visible = fields.Bool()
    keep_alive = fields.Bool()
    menu_perm = fields.Str()
    menu_sort = fields.Int()