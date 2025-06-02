from webargs import fields
from webargs.flaskparser import use_args
from marshmallow import Schema, fields, EXCLUDE

class MenuArgsSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # 忽略多余字段

    id = fields.Int(required=False, allow_none=True)
    parent_id = fields.Int(required=False, data_key='parentId')
    menu_path = fields.Str(required=True, data_key='routePath')
    component = fields.Str(required=False, data_key='component')
    redirect_url = fields.Str(required=False, data_key='redirect')
    menu_name = fields.Str(required=False, data_key='name')
    menu_icon = fields.Str(required=False, data_key='icon')
    menu_type = fields.Int(required=True, data_key='type')
    menu_visible = fields.Bool(missing=True, data_key='visible')
    keep_alive = fields.Bool(missing=True, data_key='keepAlive')
    menu_perm = fields.Str(required=False, allow_none=True, data_key='perm')
    menu_sort = fields.Int(required=False, data_key='sort')
    route_name = fields.Str(required=False, data_key='routeName')
    # params 和 alwaysShow 可选添加
    # params = fields.Dict(required=False, data_key='params')
    # alwaysshow = fields.Bool(missing=False, data_key='alwaysShow')


menu_args = {
    'id': fields.Int(required=False, allow_none=True),  # 解决 id 报错
    'parent_id': fields.Int(required=False, data_key='parentId'),
    'menu_path': fields.Str(required=True, data_key='routePath'),
    'component': fields.Str(required=False, data_key='component'),
    'redirect_url': fields.Str(required=False,allow_none=True, data_key='redirect'),
    'menu_name': fields.Str(required=False, data_key='name'),
    'menu_icon': fields.Str(required=False, data_key='icon'),
    'menu_type': fields.Int(required=True, data_key='type'),
    'menu_visible': fields.Bool(missing=True, data_key='visible'),
    'keep_alive': fields.Bool(missing=True, data_key='keepAlive'),
    'menu_perm': fields.Str(required=False, allow_none=True, data_key='perm'),
    'menu_sort': fields.Int(required=False, data_key='sort'),
    'route_name': fields.Str(required=False, data_key='routeName'),
    # 'params': fields.Dict(required=False, data_key='params'),
    'alwaysshow': fields.Bool(missing=False, data_key='alwaysShow'),
}