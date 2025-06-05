from flask.views import MethodView
from flask import jsonify, request, current_app, json
from marshmallow import ValidationError
from webargs.flaskparser import use_args

from src.core.auth import auth
from ...v1 import api_v1
from src.schemas.system_schemas import MenuSchema,DictTpyeReportSchema,DictTypeQuerySchema,DictItemSchema
from src.validators.menu_args import menu_args
from ....models.system import UserInfo,DictType,DictItem
from ....models.experiment import ExperimentReport
from sqlalchemy import select
from ....core.extensions import db
from src.schemas.experiment_schemas import ExperimentReportSchema,ExperimentReportQuerySchema
# schema 初始化
dict_type_detail_schema = DictTpyeReportSchema()  # 单项序列化
dict_type_query_schema = DictTypeQuerySchema()    # 查询参数校验和反序列化
dict_items_schema = DictItemSchema(many=True)  # 字典项序列化
dict_item_schema = DictItemSchema()  # 字典项序列化
class DictAPI(MethodView):
    """
    字典类型接口类：
    - GET /dicts/page        ：分页查询字典类型
    - GET /dicts/<id>/form   ：获取单个字典详情
    - PUT /dicts/<id>        ：更新字典类型
    """
    decorators = [auth.login_required]
    def get(self, dict_id=None):
        """
        GET 请求：
        - 如果传入 dict_id，则返回单个字典信息。
        - 否则，按条件分页查询字典列表。
        """
        if dict_id:
            # 查询单条记录并返回序列化数据
            dict_item = DictType.query.get_or_404(dict_id)
            result = dict_type_detail_schema.dump(dict_item)
            return jsonify(code='200', data=result, msg='获取信息成功！')

        # 获取并解析查询参数（分页 + 模糊查询）
        query_params = dict_type_query_schema.load(request.args)

        # 分离分页参数
        page_size = query_params.pop('page_size', 10)
        page_num = query_params.pop('page_num', 1)
      
        # 构建基础查询
        dicts_query = select(DictType)
        for key, value in query_params.items():
            if value and hasattr(DictType, key):
                dicts_query = dicts_query.where(getattr(DictType, key).like(f'%{value}%'))
     
        # 添加排序、分页
        dicts_query = dicts_query.order_by(DictType.id.desc())
        paginated = db.paginate(
            dicts_query,
            page=page_num,
            per_page=page_size,
            max_per_page=100,
            error_out=False
        )

        # 如果没有数据
        if not paginated.items:
            return jsonify(code='404', data=[], msg='没有字典信息！')

        # 序列化每项
        results = [dict_type_detail_schema.dump(item) for item in paginated.items]

        # 构造响应
        return jsonify(
            code='200',
            data={'list': results, 'total': paginated.total},
            msg='获取信息成功！'
        )

    @use_args(dict_type_detail_schema, location='json')
    def post(self, args):
        """
        POST 请求：创建新的字典类型
        """
        dict_type_data = args
        # 检查是否已存在相同的字典类型
        existing_dict = DictType.query.filter_by(code=dict_type_data['code']).first()
        if existing_dict:
            return jsonify(code='400', msg='字典类型已存在，请勿重复添加')

        # 创建新的字典类型实例
        new_dict_type = DictType(
            name=dict_type_data.get('name'),
            code=dict_type_data.get('code'),
            status=dict_type_data.get('status', True),
            remark=dict_type_data.get('remark', '')
        )
        
        # 添加到数据库
        db.session.add(new_dict_type)
        db.session.commit()
        
        return jsonify(code='200', data=dict_type_detail_schema.dump(new_dict_type), msg='添加字典成功！')

    @use_args(dict_type_detail_schema, location='json')
    def put(self, args, dict_id):
        """
        PUT 请求：更新字典类型
        """
        dict_type = DictType.query.get_or_404(dict_id)

        # 遍历传入字段更新
        for key, value in args.items():
            if hasattr(dict_type, key):
                setattr(dict_type, key, value)

        db.session.commit()
        return jsonify(code='200', data={}, msg='更新字典成功！')


class DictItemAPI(MethodView):
    def get(self, dict_code):
        """
        GET 请求：获取指定字典类型的所有字典项
        """
        dict_items = DictItem.query.filter_by(dict_code=dict_code,is_deleted=0).all()
        if not dict_items:
            return jsonify(code='404', data=[], msg='没有字典项信息！')
        # 序列化字典项
        results = dict_items_schema.dump(dict_items)
        res={
            'list': results,
            'total': len(results)
        }
        return jsonify(code='200', data=res, msg='获取字典项成功！')

class DictItemsAPI(MethodView):
    def get(self, dict_code,id):
        """
        GET 请求：获取指定字典类型的所有字典项
        """
        dict_items = DictItem.query.filter_by(id=id,is_deleted=0).scalar()
        if not dict_items:
            return jsonify(code='404', data=[], msg='没有字典项信息！')
        # 序列化字典项
        res= dict_item_schema.dump(dict_items)
        if not res:
            return jsonify(code='404', data=[], msg='没有字典项信息！')
        return jsonify(code='200', data=res, msg='获取字典项成功！')
    @use_args(dict_item_schema, location='json')
    def put(self, args, dict_code, id):
        """
        PUT 请求：更新指定字典项
        """
        dict_item = DictItem.query.filter_by(id=id, dict_code=dict_code,is_deleted=0).first_or_404()
        # 遍历传入字段更新
        for key, value in args.items():
            if hasattr(dict_item, key):
                setattr(dict_item, key, value)
        db.session.commit()
        return jsonify(code='200', data={}, msg='更新字典项成功！')
    @use_args(dict_item_schema, location='json')
    def post(self, args, dict_code):
        """
        POST 请求：创建新的字典项
        """
        item_data = args
        dict_code = item_data.get('dict_code', None)
        dict_value = item_data.get('value', None)
        #查重
        existing_item = DictItem.query.filter_by(dict_code=dict_code, value=dict_value,is_deleted=0).first()
        if existing_item:
            return jsonify(code='400', msg='字典项已存在，请勿重复添加')
       
        new_item = DictItem(
            dict_code=dict_code,
            type_id=item_data.get('type_id', None),
            label=item_data.get('label', None),
            value=dict_value,
            status=item_data.get('status', True),
            sort=item_data.get('sort', '0'),
        )
        # 添加新字典项到数据库
        db.session.add(new_item)
        db.session.commit()
        return jsonify(code='200', data=dict_item_schema.dump(new_item), msg='添加字典项成功！')
    def delete(self, dict_code,id):
        """
        DELETE 请求：删除指定字典项
        """
        dict_item = DictItem.query.filter_by(id=id, dict_code=dict_code).first_or_404()
        dict_item.is_deleted = True  # 逻辑删除
        # db.session.delete(dict_item)  # 如果需要物理删除，使用此行
        db.session.commit()
        return jsonify(code='200', data={}, msg='删除字典项成功！')


api_v1.add_url_rule('/dicts/page', view_func=DictAPI.as_view('dict_list'), methods=['GET'])
api_v1.add_url_rule('/dicts/<int:dict_id>', view_func=DictAPI.as_view('dict_edit'), methods=['PUT'])
api_v1.add_url_rule('/dicts', view_func=DictAPI.as_view('dict_create'), methods=['POST'])
api_v1.add_url_rule('/dicts/<int:dict_id>/form', view_func=DictAPI.as_view('dict_detail'), methods=['GET',])
api_v1.add_url_rule('/dicts/<string:dict_code>/items/page', view_func=DictItemAPI.as_view('dict_items'), methods=['GET'])
api_v1.add_url_rule('/dicts/<string:dict_code>/items/<int:id>/form', view_func=DictItemsAPI.as_view('dict_item_get'), methods=['GET'])
api_v1.add_url_rule('/dicts/<string:dict_code>/items/<int:id>', view_func=DictItemsAPI.as_view('dict_item_edit'), methods=['PUT','DELETE'])
api_v1.add_url_rule('/dicts/<string:dict_code>/items', view_func=DictItemsAPI.as_view('dict_item_add'), methods=['POST',])