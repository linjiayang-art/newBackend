from flask.views import MethodView
from flask import jsonify, request, current_app, json
from marshmallow import ValidationError
from webargs.flaskparser import use_args

from src.core.auth import auth
from ...v1 import api_v1
from src.schemas.test_item_schemas import TestItemBaseInfoSchema,TestItemBaseInfoUpdateSchema,TestItemBaseInfoQuery
from src.validators.menu_args import menu_args
from ....models.system import UserInfo, DictType, DictItem
from ....models.test_item import TestItemBaseInfo
from sqlalchemy import select
from ....core.extensions import db
from src.schemas.experiment_schemas import ExperimentReportSchema, ExperimentReportQuerySchema
# schema 初始化
test_item_base_info_schema = TestItemBaseInfoSchema()  # 单项序列化
test_item_base_info_query_schema = TestItemBaseInfoQuery()  # 查询参数校验和反序列化
test_items_schema = TestItemBaseInfoSchema(many=True)  # 列表序列化
#test_item_base_query_schema = TestItemBaseInfoSchema()  # 查询参数校验和反序列化
test_item_base_update_schema = TestItemBaseInfoUpdateSchema(partial=True)  # 更新参数校验和反序列化 

class TestItemBaseAPI(MethodView):
    def get(self, test_item_id=None):
        """
        获取试验项目详情或列表
        - 如果传入 test_item_id，则返回单个试验项目详情。
        - 否则，返回试验项目列表。
        """
        if test_item_id:
            # 查询单条记录并返回序列化数据
            test_item = TestItemBaseInfo.query.get_or_404(test_item_id)
            result = TestItemBaseInfoSchema().dump(test_item)
            return jsonify(code='200', data=result, msg='获取信息成功！')
        # 分页查询试验项目列表
        query_params = test_item_base_info_query_schema.load(request.args)
        page_size = int(query_params.pop('page_size', 10))
        page_num = int(query_params.pop('page_num', 1))
        # 构建基础查询
        test_items_query = select(TestItemBaseInfo)
        for key, value in query_params.items():
            if value and hasattr(TestItemBaseInfo, key):
                test_items_query = test_items_query.where(
                    getattr(TestItemBaseInfo, key).like(f'%{value}%'))
        # 添加排序、分页

        test_items_query = test_items_query.order_by(
            TestItemBaseInfo.id.desc())
        paginated = db.paginate(
            test_items_query,
            page=page_num,
            per_page=page_size,
            max_per_page=100,
            error_out=False
        )

        result = {
            'total': paginated.total,
            'page_size': paginated.per_page,
            'page_num': paginated.page,
            'pages': paginated.pages,
            'list': test_items_schema.dump(paginated.items)
        }
        return jsonify(code='200', data=result, msg='获取列表成功！')
    @use_args(test_item_base_info_schema, location='json')
    def post(self,args):
        """
        创建新的试验项目
        - 接收 JSON 数据并进行验证。
        - 如果验证通过，保存新试验项目并返回创建结果。
        """
        try:
            new_test_item = TestItemBaseInfo(**args)
            db.session.add(new_test_item)
            db.session.commit()
            result = test_item_base_info_schema.dump(new_test_item)
            return jsonify(code='200', data=result, msg='创建成功！')
        except ValidationError as err:
            return jsonify(code='400', data=err.messages, msg='数据验证失败！'), 400
    @use_args(test_item_base_update_schema, location='json',)
    def put(self, args, test_item_id):
        """
        更新试验项目
        - 接收 JSON 数据并进行验证。
        - 如果验证通过，更新指定试验项目并返回更新结果。
        """
        print(args)
        test_item = TestItemBaseInfo.query.get_or_404(test_item_id)
        for key, value in args.items():
            setattr(test_item, key, value)
        db.session.commit()
        result = test_item_base_info_schema.dump(test_item)
        return jsonify(code='200', data=result, msg='更新成功！')
    def delete(self, test_item_id):
        """
        删除试验项目
        - 根据 test_item_id 删除指定试验项目。
        """
        test_item = TestItemBaseInfo.query.get_or_404(test_item_id)
        db.session.delete(test_item)
        db.session.commit()
        return jsonify(code='200', data=None, msg='删除成功！')

api_v1.add_url_rule(
    '/testitems/list', view_func=TestItemBaseAPI.as_view('test_item_base_list'), methods=['GET', 'POST']
)
api_v1.add_url_rule(
    '/testitems/<int:test_item_id>', view_func=TestItemBaseAPI.as_view('test_item_base_detail'), methods=['GET', 'PUT', 'DELETE']
)
