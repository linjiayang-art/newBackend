from flask.views import MethodView
from flask import jsonify, request, current_app, json
from marshmallow import ValidationError
from webargs.flaskparser import use_args

from src.core.auth import auth
from ...v1 import api_v1
from src.schemas.test_item_schemas import *
from src.validators.menu_args import menu_args
from ....models.system import UserInfo, DictType, DictItem
from ....models.test_item import TestItemBaseInfo, TestSubjectInfo, TestItemInfo
from sqlalchemy import select
from ....core.extensions import db


'''
测试模型信息 API
- 获取测试模型列表或详情
'''
test_model_info_schema = TestSubjectInfoSchema()  # 单项序列化
test_model_info_query_schema = TestSubjectInfoQuerySchema()  # 查询参数校验和反序列化
test_models_schema = TestSubjectInfoSchema(many=True)  # 列表序列化
test_model_info_update_schema = TestSubjectInfoUpdateSchema(partial=True)  # 更新参数校验和反序列化
test_model_info_create_schema = TestSubjectInfoCreateSchema()  # 创建参数校验和反序列化

class TestSubjectInfoAPI(MethodView):
    decorators = [auth.login_required]
    def get(self, model_id=None):
        """
        获取测试模型详情或列表
        - 如果传入 model_id，则返回单个测试模型详情。
        - 否则，返回测试模型列表。
        """
        if model_id:
            # 查询单条记录并返回序列化数据
            test_model = TestSubjectInfo.query.get_or_404(model_id)
            result = test_model_info_schema.dump(test_model)
            return jsonify(code='200', data=result, msg='获取信息成功！')
        # 分页查询测试模型列表
        query_params = test_model_info_query_schema.load(request.args)
        page_size = int(query_params.pop('page_size', 10))
        page_num = int(query_params.pop('page_num', 1))
        # 构建基础查询
        test_models_query = select(TestSubjectInfo)
        for key, value in query_params.items():
            if value and hasattr(TestSubjectInfo, key):
                test_models_query = test_models_query.where(
                    getattr(TestSubjectInfo, key).like(f'%{value}%'))
        # 添加排序、分页
        test_models_query = test_models_query.order_by(
            TestSubjectInfo.id.desc())
        paginated = db.paginate(
            test_models_query,
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
            'list': test_models_schema.dump(paginated.items)
        }
        return jsonify(code='200', data=result, msg='获取列表成功！')

    def post(self):
        """
        创建新的测试模型
        - 接收 JSON 数据并进行验证。
        - 如果验证通过，保存新测试模型并返回创建结果。
        """
        try:
            new_test_model = test_model_info_create_schema.load(request.json)
            new_model= TestSubjectInfo(
                name=new_test_model['name'],
                name_cn=new_test_model.get('name_cn'),
                description=new_test_model.get('description'),
                #model_id=new_test_model.get('modelId')
            )
            iscopy = new_test_model.pop('iscopy', False)
            db.session.add(new_model)
            db.session.commit()
            if iscopy:
                model_id = new_test_model.get('model_id')
                #获取model_id的所有项目
                if model_id:
                    test_item = TestItemInfo.query.filter_by(test_subject_id=model_id).all()
                    for item in test_item:
                        new_item = TestItemInfo(
                            test_subject_id=new_model.id,
                            sort_order=item.sort_order,
                            test_name=item.test_name,
                            test_name_cn=item.test_name_cn,
                            test_spec=item.test_spec,
                            test_criteria=item.test_criteria,
                            sample_quantity=item.sample_quantity
                        )
                        db.session.add(new_item)
            db.session.commit()
            # 返回创建的模型信息
            result = test_model_info_schema.dump(new_model)
            return jsonify(code='200', data=result, msg='创建成功！')
        except ValidationError as err:
            return jsonify(code='400', data=err.messages, msg='数据验证失败！'), 400

'''
测试模板明细
'''
test_item_info_schema = TestItemInfoSchema()  # 单项序列化
test_item_info_query_schema = TestItemInfoQuerySchema()  # 查询参数校验和反序列化
test_items_schema = TestItemInfoSchema(many=True)  # 列表序列化
test_item_info_create_schema = TestItemInfoCreateSchema(many=True)  # 创建参数校验和反序列化
class TestItemInfoAPI(MethodView):
    decorators = [auth.login_required]
    def get(self, test_subject_id=None):
        """查询该项目下的试验模板明细,没有则返回空LIST"""
        if test_subject_id:
            # 查询单条记录并返回序列化数据
            test_item = TestItemInfo.query.filter_by(test_subject_id=test_subject_id).all()
            for i in test_item:
                print(i.__dict__)
            result_info = test_items_schema.dump(test_item)
            result = {
                'total': len(result_info),
                'list': result_info
            }
            print(result)
            return jsonify(code='200', data=result, msg='获取信息成功！')
        else:
            return jsonify(code='404', data=[], msg='没有试验模板明细信息！')

    @use_args(test_item_info_create_schema, location='json')
    def post(self, args, test_subject_id):
        """
        创建新的试验模板明细
        - 接收 JSON 数据并进行验证。
        - 如果验证通过，保存新试验模板明细并返回创建结果。
        """
        success_count = 0
        """先把之前的删了或者软删除"""
        TestItemInfo.query.filter_by(test_subject_id=test_subject_id).delete()
        db.session.commit()
        for item in args:
            try:
                item['test_subject_id'] = test_subject_id  # 设置试验模型ID
                new_test_item = TestItemInfo(**item)
                db.session.add(new_test_item)
                db.session.commit()
                success_count += 1
            except Exception as e:
                db.session.rollback()
                return jsonify(code='400', data=str(e), msg='创建失败！'), 400
        db.session.commit()
        return jsonify(code='200', data=item, msg='创建成功！, 成功创建 {} 条试验模板明细'.format(success_count))
        


'''
测试模型信息 API
- 获取测试模型列表或详情
- 创建新的测试模型
'''
# schema 初始化
test_item_base_info_schema = TestItemBaseInfoSchema()  # 单项序列化
test_item_base_info_query_schema = TestItemBaseInfoQuery()  # 查询参数校验和反序列化
test_items_basic_schema = TestItemBaseInfoSchema(many=True)  # 列表序列化
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
            'list': test_items_basic_schema.dump(paginated.items)
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
    '/testbasicitems/list', view_func=TestItemBaseAPI.as_view('test_item_base_list'), methods=['GET', 'POST']
)
api_v1.add_url_rule(
    '/testbasicitems/<int:test_item_id>', view_func=TestItemBaseAPI.as_view('test_item_base_detail'), methods=['GET', 'PUT', 'DELETE']
)

api_v1.add_url_rule(
    '/testsubjects/list', view_func=TestSubjectInfoAPI.as_view('test_subject_info_list'), methods=['GET', 'POST']
)
api_v1.add_url_rule(
    '/testsubjects/<int:subject_id>', view_func=TestSubjectInfoAPI.as_view('test_subject_info_detail'), methods=['GET']
)
api_v1.add_url_rule(
    '/testitems/<int:test_subject_id>', view_func=TestItemInfoAPI.as_view('test_item_info_list'), methods=['GET', 'POST']
)