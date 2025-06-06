
import os

import flask
from ...core.auth import auth

from flask import Blueprint, current_app, jsonify, send_file, url_for
from flask_cors import CORS
from webargs import fields
from ...core.extensions import db

api_v1 = Blueprint('api_v1', __name__)
CORS(api_v1)
# docs.register(UserResource, blueprint='api_v1', endpoint='user_detail')
# docs.register(UserResource,blueprint='api_v1', endpoint='user_create')

# 注册 v1 版本相关蓝图或模块
from . import system,experiment  # 导入当前 v1 目录下的 system 子模块




@api_v1.route('/')
def api_v1_index():
    return 'api_v1_index'

    
                   

@api_v1.route('/user/icon')
def user_icon():
    """
    获取用户头像
    """
    avatar_path = os.path.join(current_app.config['MODEL_FILE_DIR'], 'icon.gif')
    print(avatar_path)
    with open(avatar_path, 'rb') as f:
        avatar_base64 = f.read()
    if not avatar_base64:
        avatar_base64 = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    return send_file( avatar_path , mimetype='image/gif')
@api_v1.route('/users/me')
@auth.login_required()
def users_me():
    return jsonify(code="200",
                     data={ 'userId': 2,
                        'nickname': "系统管理员",
                        'username': "admin",
                        'avatar':    'http://127.0.1:5000/api/v1/user/icon',
                        'roles': ["ROOT"],
                        'perms': [
                          "sys:menu:delete",
                          "sys:dept:edit",
                          "sys:dict_type:add",
                          "sys:dict:edit",
                          "sys:dict:delete",
                          "sys:dict_type:edit",
                          "sys:menu:add",
                          "sys:user:add",
                          "sys:role:edit",
                          "sys:dept:delete",
                          "sys:user:edit",
                          "sys:user:delete",
                          "sys:user:password:reset",
                          "sys:dept:add",
                          "sys:role:delete",
                          "sys:dict_type:delete",
                          "sys:menu:edit",
                          "sys:dict:add",
                          "sys:role:add",
                          "sys:user:query",
                          "sys:user:export",
                          "sys:user:import",
                        ],}
                    ,msg="一切ok")

@api_v1.route('/auth/captcha')
def swagger_ui():
    return jsonify(code="200",
                   data={
                        'captchaKey': "534b8ef2b0a24121bec76391ddd159f9",
                        'captchaBase64':
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAAkCAIAAADNSmkJAAAFKUlEQVR4Xu2ZXUwcVRiGV70wMWo08V5NvPXCrDbFaGpMaZW2hqQxaoiJTRsaMBCNSYtpa2JTKiFSelFa+Q/QZcMWqEhBlh+htbEpZhMrBQrlJ0hBywLLyrJ0WZbje3bqOvPNLHPWrDvdOE9ONmfe78zkzMs335wzWJhJQrBQweS/wTQ6QWgYHdoIOcecOe05O+t2WkutO+p2ZF3Ksg/YV9ZW6FATYajR3nveg60H9327r3O8c35lHgp+r05dPdJzBL73TPSQ8SaCKIxGLsPlop+K0JHrEkPuoT31e5qGmmjARACF0agYyGVNlyVm/pzZXrN9fHGcBkz0UBid+31u93i3XFFT80vN8cvHqWqih8Lo1NpUqS5vwh3vnd223VQ10UNh9NbyrcFQUK6oCawHUipSqGqiB83oBf+CXFGDMp1mS6OqiR4Ko7FexkpOrqhpHGw82nOUqiZ6KIzGrkRuorW0dJMmOy+hOCfYGzb2RBFv6HRO0gEJw/U7y+pgL1bwmTxexN6sZ31TdEwEhdG+gA+7EqyXpUO1uZH20cWL8hMTRt1N9tBXzCJrOIRoCPJpSO2RAp4HmtCdIfZ+2JWgEBN9LbR28seTGU0Zue1tMLp+YIAMSADzfvbkKX4/eb28j4YODiGin3heqmIlLja5hAUCu+nmGY3JWKvpMAlqNGgebsauBOvlqSX+JEx7p7EbTLen53XlzfmWUioqXikrc68Y8N2juJ/fyVsNChGHEE//rBANYWaZz+TRQqpLaBgNsPfDrgSpbS21YtV87IdjrlkX9JZbt5DOma2t9ITo5F+5glN22WwL/n+yDv00mw06orKxOqQ5+J04hhViwzAXETIcJDVm8uxZqktoGx2Nj9t43Wgaul/ERQiGQvtbWnDWgZYW9CXlQFjZ/7ciyHNn+Z2MexTimIeLz59TiIln0M1e+IbPpOAaDUnEYPTi6iqKxpbycs/qKo1tCslfKcffPn9enuMiPPY1vxO/ckeFQ4h46cdGqUWoidE/y54q5tPY5WDrGzQqIXot4BgchEE57e00IMCw2/1qZSVO/7SjA78o9INzcxsbrL+fnTnDDh9mmZn8F30oG1Hm+nABv5mQMopDS/h1HxtqTzWbABMe9sxpPoe9zezeOo1GELqWhPS8t46M0IAYHbdvR1aHbaOjbjfLz2eFhez6dba4yAfgF30o0BFVE8+Mjh/wFxPI+I5mAEHU6Ls+38vhTFwOBGhMDF8gkFpbC5ffsdv/uBs6dIj19dExEtARVXv9YNbop8NFY3aZ6gRRo+tu3IBHnzmdNCBMXldXJKPfL74WzWUJRE+coDUknqsOdZXQbAJYwluVTbOZI3Qt8GFzMwxyjo3RgBiN4fr+elXVpZGRLWXl6PdOTtJBSlBDUK/lnIrjOlrtqWYTQDJaF6FrTXu9sOa1ysrVoM5HVE1GFxZQcyJ/p+xzv6K/rbr6N6+XDpUBl0tKFIrbz78qWB6YnWFMCBld4XLBms+7df75ook/GNzb0GCV7U1Qfz9p64TyQWNjYD3qe9rj4SMJtQP3MyjSDPzWIRHPjH7X4YAvfXoPuyZf9Pbi3PcuXIh4mp3NllYC6XY79C+jl2o8PBipxjnBttn4MgMNnWgfcRJGPI2OL8hTj3LloIlmRicvBhiNykvecpqoa3RSY4DRcLAwyicuOepVR1JjgNFYHWONHL04czTX0UmNAUYD7Pr+xc4wqTHGaBb2OtZvHUmNYUazcA2J6etdUmOk0f8rTKMTxF91RG0D1SwYGwAAAABJRU5ErkJggg==",
                   },  msg= "一切ok",
                   )

# menu_view = MenusAPI.as_view('menu_resource')
# api_v1.add_url_rule(
#     '/menus', defaults={'menu_id': None}, view_func=menu_view, methods=['GET'])
# api_v1.add_url_rule('/menus', view_func=menu_view, methods=['POST'])
# api_v1.add_url_rule('/menus/<int:menu_id>',
#                     view_func=menu_view, methods=['GET', 'PUT', 'DELETE'])
# token_view = TokenAPI.as_view('token_resource')
# api_v1.add_url_rule('/token', view_func=token_view, methods=['POST'])
# api_v1.add_url_rule('/userinfo/<int:user_id>',
#                     view_func=UserResource.as_view('user_detail'), methods=['GET'])
# api_v1.add_url_rule(
#     '/users', view_func=UserResource.as_view('user_create'), methods=['POST'])
# router_view = RoutesAPI.as_view('router_resource')
# api_v1.add_url_rule('menus/routes', view_func=router_view, methods=['GET'])
