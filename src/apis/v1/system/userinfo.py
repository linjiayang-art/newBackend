from flask import Flask, jsonify,current_app
from flask.views import MethodView
from ....models.system import UserInfo, Menu
from ....schemas.system_schemas import UserInfoSchema
from ....validators.user_args import user_args
from ....core.extensions import db,spec
from ...v1 import api_v1
from webargs.flaskparser import use_args

user_schema = UserInfoSchema()
users_schema = UserInfoSchema(many=True)
class UserResource(MethodView):
    def get(self, user_id):
        user = UserInfo.query.get_or_404(user_id)
        return jsonify(users_schema .dump(user))
    @use_args(user_args)
    def post(self,args):
        print(args)
        new_user = UserInfo(**args)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            code=200, msg='User created successfully', data=user_schema.dump(new_user)
        ), 200


api_v1.add_url_rule('/userinfo/<int:user_id>',
                    view_func=UserResource.as_view('user_detail'), methods=['GET'])
api_v1.add_url_rule(
    '/users', view_func=UserResource.as_view('user_create'), methods=['POST'])

# spec.components.schema("UserInfoSchema", schema=UserInfoSchema)
# spec.path(resource=UserResource, app=current_app, path="/userinfo/{user_id}")

