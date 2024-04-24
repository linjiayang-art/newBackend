from flask import Blueprint,current_app

index_bp = Blueprint('index', __name__)



@index_bp.route('/index')
def index():
    return 'index'
