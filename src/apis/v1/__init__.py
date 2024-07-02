
from flask import Blueprint
from flask_cors import CORS
from webargs import fields
from flask_apispec import use_kwargs, marshal_with
from .system.userinfo import UserResource
api_v1=Blueprint('api_v1',__name__)
CORS(api_v1)

@api_v1.route('/')
def api_v1_index():
    return 'api_v1_index'

@api_v1.route('/pets')
@use_kwargs({'species': fields.Str()})
def list_pets(**kwargs):
    return 'ok'
api_v1.add_url_rule('/userinfo/<int:user_id>', view_func=UserResource.as_view('user_detail'))
api_v1.add_url_rule('/users', view_func=UserResource.as_view('user_create'))
from src.apis.v1 import system 