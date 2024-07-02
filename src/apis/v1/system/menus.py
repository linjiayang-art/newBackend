from flask.views import MethodView
from flask import jsonify, request, current_app, json

from ....models.system import UserInfo, Menu
from sqlalchemy import select
from ....core.extensions import db
# from ....core.extensions import db, csrf
# from backend.apis.auth.auth import generate_token, auth_required
from flask_wtf.csrf import generate_csrf
# from backend.forms.systemform import MenuFrom
# from apispec import APISpec


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