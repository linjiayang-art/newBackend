from marshmallow import EXCLUDE, Schema, fields
from .base_schemas import BaseSchema


'''实验模板schemas三个查询,实体,更新,创建'''

class TestSubjectInfoCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # 忽略前端多传的字段
    """实验模型信息创建参数校验和反序列化
    """
    name = fields.Str(required=True, description="试验模型名称", data_key='name')
    name_cn = fields.Str(required=False, description="试验模型中文名", data_key='nameCn')
    description = fields.Str(required=False, description="试验模型描述", data_key='description')
    iscopy = fields.Boolean(required=False, description="是否复制", data_key='isCopy', default=False)
    model_id = fields.Int(required=False, description="模型ID", data_key='modelId', allow_none=True)

class TestSubjectInfoSchema(Schema):
    """实验模型信息序列化
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, description="试验模型名称", data_key='name')
    name_cn = fields.Str(required=False, description="试验模型中文名", data_key='nameCn')
    description = fields.Str(required=False, description="试验模型描述", data_key='description')
    created_at = fields.DateTime(dump_only=True, required=False)
    updated_at = fields.DateTime(dump_only=True, required=False)
class TestSubjectInfoQuerySchema(BaseSchema):
    """
    查询参数校验和反序列化
    """
    name = fields.Str(required=False, data_key='name')
    name_cn = fields.Str(required=False, data_key='nameCn')
    description = fields.Str(required=False, allow_none=True, data_key='description')
    page_size = fields.Int(missing=10, data_key='pageSize', description="每页数量")
    page_num = fields.Int(missing=1, data_key='pageNum', description="页码")
class TestSubjectInfoUpdateSchema(Schema):
    """实验模型信息更新参数校验和反序列化
    """
    class Meta:
        unknown = EXCLUDE  # 忽略前端多传的字段
    name = fields.Str(required=False, data_key='name')
    name_cn = fields.Str(required=False, data_key='nameCn')
    description = fields.Str(required=False, allow_none=True, data_key='description')
    

'''
实验模板明细schemas三个查询,实体,更新,创建
'''
class TestItemInfoCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # 忽略前端多传的字段
    """实验模板明细信息创建参数校验和反序列化
    """
    sort_order = fields.Int(required=False, allow_none=True, description="排序", data_key='sort_order')
    test_subject_id = fields.Int(required=False, description="试验模型ID", data_key='testSubjectId')
    test_name = fields.Str(required=True, description="试验项目", data_key='testName')
    test_name_cn = fields.Str(required=False, description="试验项目中文名", data_key='testNameCn')
    test_spec = fields.Str(required=True, description="试验标准号及名称", data_key='testSpec')
    test_criteria = fields.Str(required=False, allow_none=True, description="目标要求（评定依据）", data_key='testCriteria')
    sample_quantity = fields.Str(required=False, allow_none=True, description="样品数量", data_key='sampleQuantity')

class TestItemInfoSchema(Schema):
    id = fields.Int(dump_only=True)
    test_name = fields.Str(required=True, description="试验项目", data_key='testName')
    sort_order = fields.Int(required=False, description="排序", data_key='sort_order')
    test_name_cn = fields.Str(required=False, description="试验项目中文名", data_key='testNameCn')
    test_spec = fields.Str(required=True, description="试验标准号及名称", data_key='testSpec')
    test_criteria = fields.Str(required=False, description="目标要求（评定依据）", data_key='testCriteria')
    sample_quantity = fields.Str(required=False, description="样品数量", data_key='sampleQuantity')
    created_at = fields.DateTime(dump_only=True, required=False)
    updated_at = fields.DateTime(dump_only=True, required=False)


class TestItemInfoQuerySchema(BaseSchema):
    """
    查询参数校验和反序列化
    """
    test_subject_id = fields.Int(required=False, data_key='testSubjectId')
    sort_order= fields.Int(required=False, allow_none=True, description="排序", data_key='sort_order')
    test_name = fields.Str(required=False, data_key='testName')
    test_name_cn = fields.Str(required=False, data_key='testNameCn')
    test_spec = fields.Str(required=False, data_key='testSpec')
    test_criteria = fields.Str(required=False, allow_none=True, data_key='testCriteria')
    sample_quantity = fields.Str(required=False, allow_none=True, data_key='sampleQuantity')
    page_size = fields.Int(missing=10, data_key='pageSize', description="每页数量")
    page_num = fields.Int(missing=1, data_key='pageNum', description="页码")


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
