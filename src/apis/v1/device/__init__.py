from flask.views import MethodView
from flask import jsonify, request, current_app, json
from marshmallow import ValidationError
from webargs.flaskparser import use_args

from src.core.auth import auth
from ...v1 import api_v1
from src.schemas.system_schemas import MenuSchema
from src.validators.menu_args import menu_args
from ....models.system import UserInfo
from ....models.devicemodel import Device
from sqlalchemy import select
from ....core.extensions import db
from src.schemas.device_schemas import DeviceSchema, DeviceQuerySchema
device_schema = DeviceSchema()
device_schemas = DeviceSchema(many=True)
device_query_schema = DeviceQuerySchema()


class DeviceAPI(MethodView):
    decorators = [auth.login_required]
    def get(self, device_id=None):
        if device_id:
            device = Device.query.get_or_404(device_id)
            res = device_schema.dump(device)
            return jsonify(code='200', data=res, msg='获取信息成功！')
        
        query_params = device_query_schema.load(request.args)
        devices_query = select(Device)
      
        # 分离分页参数
        page_size = query_params.pop('page_size', 10)
        page_num = query_params.pop('page_num', 1)
        
        # 处理其他查询参数，统一模糊查询
        for key, value in query_params.items():
            if value and hasattr(Device, key):
                devices_query = devices_query.where(getattr(Device, key).like(f'%{value}%'))
        
        # 分页处理
        devices_query = devices_query.order_by(Device.id.asc())
        devices = db.paginate(
            devices_query,
            page=page_num,
            per_page=page_size,
            max_per_page=100,
            error_out=False
        )
        if not devices.items:
            return jsonify(code='404', data=[], msg='没有设备信息！')
        results = device_schemas.dump(devices.items)
        return jsonify(code='200', data= {'list': results, 'total':  devices.total},msg='获取信息成功！')

api_v1.add_url_rule(
    '/device/infos', view_func=DeviceAPI.as_view('device_api'), methods=['GET']
)