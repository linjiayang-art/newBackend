
from flask import Blueprint
from flask_cors import CORS

api_v1=Blueprint('api_v1',__name__)
CORS(api_v1)

@api_v1.route('/')
def api_v1_index():
    return 'api_v1_index'

from src.apis.v1 import system 