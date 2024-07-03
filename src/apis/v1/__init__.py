
from flask import Blueprint
from flask_cors import CORS
from webargs import fields

from ...core.extensions import db

api_v1=Blueprint('api_v1',__name__)
CORS(api_v1)

@api_v1.route('/')
def api_v1_index():
    return 'api_v1_index'

#docs.register(UserResource, blueprint='api_v1', endpoint='user_detail')
# docs.register(UserResource,blueprint='api_v1', endpoint='user_create')
from src.apis.v1 import system 