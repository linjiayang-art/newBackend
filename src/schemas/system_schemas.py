from marshmallow import Schema, fields

class UserInfoSchema(Schema):
    id = fields.Int(dump_only=True)
    userno = fields.Str(required=True)
    username = fields.Str(required=True)
    password_hash = fields.Str(load_only=True)
    email = fields.Email(required=True)

class MenuSchema(Schema):
    id = fields.Int(dump_only=True)
    parent_id = fields.Int(data_key='parentId')
    menu_path = fields.Str(data_key='routePath')
    component = fields.Str()
    redirect_url = fields.Str(data_key='redirect')
    menu_name = fields.Str(data_key='name')
    menu_icon = fields.Str(data_key='icon')
    menu_type = fields.Int(data_key='type')
    menu_visible = fields.Bool(data_key='visible')
    keep_alive = fields.Bool(data_key='keepAlive')
    menu_perm = fields.Str(data_key='perm')
    menu_sort = fields.Int(data_key='sort')

