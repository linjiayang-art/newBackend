from flask.views import MethodView
from flask import jsonify, request, current_app, json
from marshmallow import ValidationError
from webargs.flaskparser import use_args

from src.core.auth import auth
from ...v1 import api_v1
from src.schemas.system_schemas import MenuSchema
from src.validators.menu_args import menu_args
from ....models.system import UserInfo
from ....models.experiment import ExperimentReport
from sqlalchemy import select
from ....core.extensions import db
from src.schemas.experiment_schemas import ExperimentReportSchema,ExperimentReportQuerySchema

experiment_report_schema = ExperimentReportSchema()
excperiment_report_query_schema = ExperimentReportQuerySchema()

class ExperimentReportAPI(MethodView):
    decorators = [auth.login_required]
    def get(self, report_id=None):
        if report_id:
            report = ExperimentReport.query.get_or_404(report_id)
            res= experiment_report_schema.dump(report)
            return jsonify(code='200', data=res, msg='获取信息成功！')
        query_params = excperiment_report_query_schema.load(request.args)
        reports_query = select(ExperimentReport)
        #单独拎出来page_size和page_num
        page_size = query_params.pop('page_size', 10)
        page_num = query_params.pop('page_num', 1)
        # 处理其他查询参数,统一模糊查询
        for key, value in query_params.items():
            if value:
                if hasattr(ExperimentReport, key):
                    reports_query = reports_query.where(getattr(ExperimentReport, key).like(f'%{value}%'))
        # 分页处理
        reports_query = reports_query.order_by(ExperimentReport.id.desc())  # 按照id降序排列
        reports = db.paginate(
            reports_query,
            page=page_num,
            per_page=page_size,
            max_per_page=100,  # 设置最大每页数量
            error_out=False  # 如果页数超出范围，返回空列表而不是404错误
        )
        if not reports:
            return jsonify(code='404', data=[], msg='没有实验报告信息！')
        results= []
        for report in reports:
            new_res=experiment_report_schema.dump(report)
            results.append(new_res)
        return jsonify(code='200', data=results, msg='获取信息成功！')
    def put(self, report_id):
        report = ExperimentReport.query.get_or_404(report_id)
        try:
            data = experiment_report_schema.load(request.json, partial=True)
        except ValidationError as err:
            return jsonify(code='400', msg='参数错误', data=err.messages), 400
        for key, value in data.items():
            setattr(report, key, value)
        db.session.commit()
        res = experiment_report_schema.dump(report)
        return jsonify(code='200', data=res, msg='更新成功！')

api_v1.add_url_rule('/experiment/report', view_func=ExperimentReportAPI.as_view('experiment_report'), methods=['GET'])
api_v1.add_url_rule('/experiment/report/<int:report_id>', view_func=ExperimentReportAPI.as_view('experiment_report_detail'), methods=['GET', 'PUT'])