
from flask import Blueprint
from flask_cors import CORS
from webargs import fields
from flask_apispec import use_kwargs, marshal_with
api_v1=Blueprint('api_v1',__name__)
CORS(api_v1)

@api_v1.route('/')
def api_v1_index():
    return 'api_v1_index'

@api_v1.route('/pets')
@use_kwargs({'species': fields.Str()})
def list_pets(**kwargs):
    return 'ok'

from src.apis.v1 import system 