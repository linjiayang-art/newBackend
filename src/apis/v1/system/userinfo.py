from flask import Flask, jsonify
from flask.views import MethodView
from ....models.system import UserInfo, Menu
from ....schemas.system_schemas import UserInfoSchema
from ....validators import user_args
from flask_apispec import use_kwargs, marshal_with
from ....core.extensions import db,docs

class UserResource(MethodView):
    @marshal_with(UserInfoSchema)
    def get(self, user_id):
        user = UserInfo.query.get_or_404(user_id)
        return user
    
    @use_kwargs(user_args, location='json')
    @marshal_with(UserInfoSchema)
    def post(self, **kwargs):
        new_user = UserInfo(**kwargs)
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201
# api_v1.add_url_rule('/users/<int:user_id>', view_func=UserResource.as_view('user_detail'),methods=['GET'])
# api_v1.add_url_rule('/users', view_func=UserResource.as_view('user_create'),methods=['POST'])

