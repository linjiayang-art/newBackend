from marshmallow import Schema, fields
from .base_schemas import BaseSchema
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
    route_name = fields.Str(data_key='routeName')

class DictTypeQuerySchema(BaseSchema):
    type_code = fields.Str(data_key='typeCode')
    keywords = fields.Str(data_key='keywords', allow_none=True)  # 允许为空
    name= fields.Str(data_key='name', allow_none=True)  # 允许为空
'''
    name = Column(String(255))
    code = Column(String(255))
    status = Column(Boolean, default=True)
    remark = Column(String(255))
'''
class DictTpyeReportSchema(Schema):
    id = fields.Int(data_key='id')
    code = fields.Str(data_key='dictCode', required=True)
    name = fields.Str(data_key='name', required=True)
    status = fields.Integer(data_key='status', default=True)
    remark = fields.Str(data_key='remark', allow_none=True)  # 允许为空
    
class DictItemSchema(Schema):
    id = fields.Int()
    dict_code = fields.Str(data_key='dictCode', required=True)
    label= fields.Str(data_key='label', required=True)
    value= fields.Str(data_key='value', required=True)
    sort= fields.Int(data_key='sort', required=True)
    status = fields.Int(data_key='status', default=1)  # 默认值为1
    tag_type= fields.Str(data_key='tagType', allow_none=True)  # 允许为空

