from flask.views import MethodView
from flask import jsonify, request, current_app, json
from webargs.flaskparser import use_args
from ...v1 import api_v1
from src.schemas.system_schemas import MenuSchema
from src.validators import menu_args
from ....models.system import UserInfo, Menu
from sqlalchemy import select
from ....core.extensions import db
# from ....core.extensions import db, csrf
# from backend.apis.auth.auth import generate_token, auth_required
from flask_wtf.csrf import generate_csrf
# from ....flask_httpauth import auth
# from backend.forms.systemform import MenuFrom
# from apispec import APISpec
menu_schema = MenuSchema()
menus_schema = MenuSchema(many=True)
from ....core.auth import generate_token

def generate_menu( menu_items: list, parent_id: int):
    result = []
    for p_m in menu_items:
        p_m = dict(p_m.menu_dict)
        if p_m['parent_id'] == parent_id:
            submenu =generate_menu(menu_items, p_m['id'])
            if submenu:
                p_m['child'] = submenu
            result.append(p_m)
    return result

class MenusAPI(MethodView):
    def get(self, menu_id=None):
        if menu_id:
            menu = Menu.query.get_or_404(menu_id)
            return jsonify(code=200,data=menu_schema.dump(menu),msg='获取信息成功！')
        else:
            menus = db.session.execute(select(Menu).filter_by(is_deleted=0)).scalars().all()
            menus = generate_menu(menus, 0)
            return jsonify(code=200, data=menus,msg='好的')
    @use_args(menu_args, location='json')
    def post(self, args):
        menu = menu_schema.load(args)
        db.session.add(menu)
        db.session.commit()
        return jsonify(menu_schema.dump(menu)), 201

    @use_args(menu_args, location='json')
    def put(self, args, menu_id):
        menu = Menu.query.get_or_404(menu_id)
        menu = menu_schema.load(args, instance=menu)
        db.session.commit()
        return jsonify(menu_schema.dump(menu))

    def delete(self, menu_id):
        menu = Menu.query.get_or_404(menu_id)
        db.session.delete(menu)
        db.session.commit()
        return '', 204



class TokenAPI(MethodView):
    def post(self):
        data = request.get_json()
        data = dict(data)
        userno = data.get('userno', None)
        password = data.get('password', None)
        if userno is None or password is None:
            return jsonify(code='401', msg='请完善表单后再提交')

        user = select(UserInfo).filter_by(userno=userno, is_deleted=False)
        user = db.session.execute(user).scalar()
        if user is None:
            return jsonify(code='401', msg='用户不存在,请检查用户编号是否正确')
        if user.validate_password(password=password) == False:
            return jsonify(code='401', msg='用户密码错误,请检查用户密码否正确')

        token_data = generate_token(user=user)
        token, expiration = token_data[0], token_data[1]
        csrf_token = generate_csrf(current_app.config['SECRET_KEY'])
        data = {
            'access_token':token,
            'status_text': expiration,
            'csrf_token': csrf_token
        }
        return jsonify(code=200, msg='登录成功', data=data)
    
# Register the resource with the blueprint
menu_view = MenusAPI.as_view('menu_resource')
api_v1.add_url_rule('/menus', defaults={'menu_id': None}, view_func=menu_view, methods=['GET'])
api_v1.add_url_rule('/menus', view_func=menu_view, methods=['POST'])
api_v1.add_url_rule('/menus/<int:menu_id>', view_func=menu_view, methods=['GET', 'PUT', 'DELETE'])
token_view = TokenAPI.as_view('token_resource')
api_v1.add_url_rule('/token', view_func=token_view, methods=['POST'])