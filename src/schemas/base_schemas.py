from marshmallow import Schema, fields

class BaseSchema(Schema):
    page_size = fields.Integer(data_key="pageSize")
    mpage_num = fields.Integer(data_key="pageNum")
  