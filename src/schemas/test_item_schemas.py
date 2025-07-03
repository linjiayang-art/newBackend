from marshmallow import EXCLUDE, Schema, fields
from .base_schemas import BaseSchema

class TestItemBaseInfoQuery(BaseSchema):
    """
    查询参数校验和反序列化
    """
    test_name = fields.Str(required=False, data_key='testName')
    test_name_cn = fields.Str(required=False, data_key='testNameCn')
    test_spec = fields.Str(required=False, data_key='testSpec')
    test_criteria = fields.Str(required=False, allow_none=True, data_key='testCriteria')
    sample_quantity = fields.Str(required=False, allow_none=True, data_key='sampleQuantity')
    page_size = fields.Int(missing=10, data_key='pageSize', description="每页数量")
    page_num = fields.Int(missing=1, data_key='pageNum', description="页码")


class TestItemBaseInfoSchema(Schema):
    id = fields.Int(dump_only=True)
    test_name = fields.Str(required=True, description="试验项目",data_key='testName')
    test_name_cn = fields.Str(required=True, description="试验项目",data_key='testNameCn')
    test_spec = fields.Str(required=True, description="试验标准号及名称",data_key='testSpec')
    test_criteria = fields.Str(required=False, description="目标要求（评定依据）",data_key='testCriteria')
    sample_quantity = fields.Str(required=False, description="样品数量",data_key='sampleQuantity')
    created_at = fields.DateTime(dump_only=True,required=False)
    updated_at = fields.DateTime(dump_only=True,required=False)


class TestItemBaseInfoUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # 忽略前端多传的字段
    test_name = fields.Str(required=False, data_key='testName')
    test_name_cn = fields.Str(required=False, data_key='testNameCn')
    test_spec = fields.Str(required=False, data_key='testSpec')
    test_criteria = fields.Str(required=False, allow_none=True, data_key='testCriteria')
    sample_quantity = fields.Str(required=False, allow_none=True, data_key='sampleQuantity')
