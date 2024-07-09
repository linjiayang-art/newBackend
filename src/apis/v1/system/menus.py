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
# from backend.forms.systemform import MenuFrom
# from apispec import APISpec
menu_schema = MenuSchema()
menus_schema = MenuSchema(many=True)


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
        username = data.get('username')
        password = data.get('password')
        return jsonify({''})
        user = UserInfo.query.filter_by(username=username).first()
        if user is None or not user.verify_password(password):
            return jsonify({'message': '用户名或密码错误'}), 401
        token = user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})
    
# Register the resource with the blueprint
menu_view = MenusAPI.as_view('menu_resource')
api_v1.add_url_rule('/menus', defaults={'menu_id': None}, view_func=menu_view, methods=['GET'])
api_v1.add_url_rule('/menus', view_func=menu_view, methods=['POST'])
api_v1.add_url_rule('/menus/<int:menu_id>', view_func=menu_view, methods=['GET', 'PUT', 'DELETE'])