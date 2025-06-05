from flask.views import MethodView
from flask import jsonify, request, current_app, json
from marshmallow import ValidationError
from webargs.flaskparser import use_args
from ...v1 import api_v1
from src.schemas.system_schemas import MenuSchema
from src.validators.menu_args import menu_args
from ....models.system import UserInfo, Menu,SysRoleMenu,SysUserRole
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



from ....core.auth import generate_token,auth
from webargs import fields
def generate_menu( menu_items: list, parent_id: int):
    result = []
    for p_m in menu_items:
        p_m = dict(p_m.menu_dict)
        if p_m['parent_id'] == parent_id:
            submenu =generate_menu(menu_items, p_m['id'])
            if submenu:
                p_m['children'] = submenu
            result.append(p_m)
    return result

def generate_menu_options( menu_items: list, parent_id: int):
    result = []
    for p_m in menu_items:
        try:
            value= p_m.id
            label = p_m.menu_name
        except AttributeError:
            value = p_m['id']
            label = p_m['menu_name']
        
        res ={
            'value': str(value),
            'label': label,
        }
        if p_m.parent_id == parent_id:
            submenu =generate_menu_options(menu_items, p_m.id)
            if submenu:
                res['children'] = submenu

            result.append(res)
    return result

class MenusAPI(MethodView):
    def get(self, menu_id=None):
        if menu_id:
            menu = Menu.query.get_or_404(menu_id)
            return jsonify(code='200', data=menu_schema.dump(menu), msg='获取信息成功！')
            menu_info=menu.menu_dict
            menu_info['parentId'] = str(menu_info['parent_id'])
            return jsonify(code='200',data=menu_info,msg='获取信息成功！')
        else:
            query_model= select(Menu).filter_by(is_deleted=0)
            keywords = request.args.get('keywords', None)
            if keywords:
                query_model = query_model.filter(Menu.menu_name.like(f'%{keywords}%'))
            query_model = query_model.order_by(Menu.menu_sort.asc())
            menus = db.session.execute(query_model).scalars().all()
            menus = generate_menu(menus, 0)
            new_menus = []
            for m in menus:
                new_menu= dict(m)
            return jsonify(code="200", data=menus,msg='获取数据成功')
    @use_args(menu_args ,location='json')
    def post(self, args):
        menu_data = args
        id = menu_data.get('id', None)
        if id is not None:
            return jsonify(code='400', msg='ID字段不允许在添加时提供，请使用PUT方法更新菜单')
        field_names = {col.name for col in Menu.__table__.columns}
        valid_data = {k: v for k, v in menu_data .items() if k in field_names}
        menu = {**valid_data, 'is_deleted': 0}  # 添加默认值
        
        id=db.session.query(Menu.id).order_by(Menu.id.desc()).first()
        if id is not None:
            menu['id'] = id[0] + 1
        print(menu)
        new_menu = Menu(**menu)
        db.session.add(new_menu)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while adding menu: {e}")
            return jsonify(code='500', msg='添加失败，请检查数据是否正确', error=str(e))
        return jsonify(code='200', msg='添加成功', data=menu_schema.dump(new_menu))


    @use_args(menu_args, location='json')
    def put(self, args, menu_id):
        menu = Menu.query.get_or_404(menu_id)
            # 手动赋值更新字段
        for key, value in args.items():
            setattr(menu, key, value)
        db.session.commit()

        return jsonify(code='200', msg='更新成功', data=menu_schema.dump(menu))

    def delete(self, menu_id):
        menu = Menu.query.get_or_404(menu_id)
        db.session.delete(menu)
        db.session.commit()
        return '', 204

class TokenAPI(MethodView):
    def post(self):
        form_data = request.form.to_dict()  # 获取表单数据
  
        if not form_data:
            return jsonify(code='401', msg='请完善表单后再提交')
        userno = form_data.get('username', None)
        password = form_data.get('password', None)
        # data = request.get_json()
        # data = dict(data)
        # userno = data.get('userno', None)
        # password = data.get('password', None)
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
            'tokenType': 'Bearer',
            'accessToken':token,
            'status_text': expiration,
            'csrf_token': csrf_token
        }
        return jsonify(code="200", msg='登录成功', data=data)

class RoutesAPI(MethodView):
    decorators = [auth.login_required]
    def get(self):
        user_info:UserInfo=auth.current_user() 
        roleresult=SysUserRole.query.filter_by(user_id=user_info.id).all()
        roleids=[role.role_id for role in roleresult]
        
        meun_select=select(Menu)\
                                .join(SysRoleMenu,Menu.id== SysRoleMenu.menu_id)\
                                .filter(SysRoleMenu.role_id.in_(roleids)).filter_by(is_deleted=0).order_by(Menu.id.asc())
        main_menus = db.session.execute(meun_select)
        menu_orgin_list = []
        for p_m in main_menus.scalars():
            menu_orgin_list.append(p_m)
        a=  self.generate_menu(menu_orgin_list,0,roles=['admin'])
        return jsonify(code='200', msg='一切ok', data=a)
    def generate_menu( self,menu_items: list, parent_id: int,roles:list=[]):
        result = []
        for p_m in menu_items:
            router_dict=dict(p_m.router_dict)
            router_dict['meta']['roles']=roles
            if int(p_m.parent_id) == parent_id:
                submenu = self.generate_menu(menu_items,int(p_m.id),roles)
                if submenu:
                    router_dict['children'] = submenu
                    
                result.append(router_dict)
        return result

class MenuOptionsAPI(MethodView):
    decorators = [auth.login_required]
    def get(self):
        # 获取所有菜单选项
        menu_options = Menu.query.filter_by(is_deleted=0).all()
        #格式value: id, label: menu_name ,需要遍历生成子节点
        menu_options_list = generate_menu_options(menu_options, 0)
        return jsonify(code='200', msg='获取菜单选项成功', data=menu_options_list)

       

# register the blueprint
menu_view = MenusAPI.as_view('menu_resource')
api_v1.add_url_rule(
    '/menus', defaults={'menu_id': None}, view_func=menu_view, methods=['GET'])
api_v1.add_url_rule('/menus', view_func=menu_view, methods=['POST'])
api_v1.add_url_rule('/menus/<int:menu_id>',
                    view_func=menu_view, methods=['GET', 'PUT', 'DELETE'])
token_view = TokenAPI.as_view('token_resource')
api_v1.add_url_rule('/auth/login', view_func=token_view, methods=['POST'])

router_view = RoutesAPI.as_view('router_resource')
api_v1.add_url_rule('menus/routes', view_func=router_view, methods=['GET'])

menu_options_view = MenuOptionsAPI.as_view('menu_options_resource')
api_v1.add_url_rule(
    'menus/options', view_func=menu_options_view, methods=['GET'])
# Register the resource with the blueprint
# menu_view = MenusAPI.as_view('menu_resource')
# api_v1.add_url_rule('/menus', defaults={'menu_id': None}, view_func=menu_view, methods=['GET'])
# api_v1.add_url_rule('/menus', view_func=menu_view, methods=['POST'])
# api_v1.add_url_rule('/menus/<int:menu_id>', view_func=menu_view, methods=['GET', 'PUT', 'DELETE'])
# token_view = TokenAPI.as_view('token_resource')
# api_v1.add_url_rule('/token', view_func=token_view, methods=['POST'])