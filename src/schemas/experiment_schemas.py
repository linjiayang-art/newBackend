from marshmallow import Schema, fields

from src.schemas.base_schemas import BaseSchema

class ExperimentReportSchema(Schema):
    id = fields.Int()
    name = fields.Str(data_key="name")
    model = fields.Str(data_key="model")
    test_type = fields.Str(data_key="testType")
    report_number = fields.Str(data_key="reportNumber")
    file_url= fields.Str(data_key="fileUrl")


class ExperimentReportQuerySchema(BaseSchema):
    name = fields.Str()
    report_number = fields.Str(data_key="reportNumber")
    test_type = fields.Str(data_key="testType")
