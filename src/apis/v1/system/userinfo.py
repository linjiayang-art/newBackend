from flask import Flask, jsonify,current_app
from flask.views import MethodView
from ....models.system import UserInfo, Menu
from ....schemas.system_schemas import UserInfoSchema
from ....validators import user_args
from ...v1 import api_v1
from ....core.extensions import db

class UserResource(MethodView):
    def get(self, user_id):
        user = UserInfo.query.get_or_404(user_id)
        return jsonify(UserInfoSchema().dump(user))

    def post(self):
        args = user_args.parse_args()
        new_user = UserInfo(**args)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(UserInfoSchema().dump(new_user)), 201

api_v1.add_url_rule('/userinfo/<int:user_id>', view_func=UserResource.as_view('user_detail'),methods=['GET'])
api_v1.add_url_rule('/users', view_func=UserResource.as_view('user_create'),methods=['POST'])
from ....core.extensions  import spec

# spec.components.schema("UserInfoSchema", schema=UserInfoSchema)
# spec.path(resource=UserResource, app=current_app, path="/userinfo/{user_id}")