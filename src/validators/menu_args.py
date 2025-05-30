from webargs import fields
from webargs.flaskparser import use_args

menu_args = {
    'parent_id': fields.Int(required=False),
    'menu_path': fields.Str(required=True),
    'component': fields.Str(required=True),
    'redirect_url': fields.Str(required=False),
    'menu_name': fields.Str(required=True),
    'menu_icon': fields.Str(required=False),
    'menu_type': fields.Str(required=True),
    'menu_name': fields.Str(required=False),
    'menu_visible': fields.Bool(missing=True),
    'keep_alive': fields.Bool(missing=True),
    'menu_perm': fields.Str(required=False),
    'menu_sort': fields.Int(required=False)
}