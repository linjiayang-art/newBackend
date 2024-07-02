from flask import Flask

from src.core.extensions import  db,docs
from .views.index import index_bp
from src.core.errors import register_errors
from src.core.request import register_request_handlers
from src.core.logging import register_logging
from src.core.commands import register_commands
from src.settings import config,basedir
import os
from src.apis.v1 import api_v1
from .views.file_server import file_bp
def init_flie():
    LOG_DIR=os.path.join(basedir, 'logs')
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    FILE_DIR=os.path.join(basedir,'uploads')
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)

    FILE_DIR=os.path.join(basedir,'modelfile')
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)

    CACHEFILE_DIR=os.path.join(basedir,'cachefile')
    if not os.path.exists(CACHEFILE_DIR):
        os.makedirs(CACHEFILE_DIR)



def create_app(config_name):
    app=Flask('src')
    #buleprints
    app.register_blueprint(index_bp,url_prefix='/index')
    app.register_blueprint(api_v1,url_prefix='/api/v1')
    app.register_blueprint(file_bp,url_prefix='/file')
    
    init_flie()
    app.config.from_object(config[config_name])
    #extensions
    db.init_app(app)
    docs.init_app(app)

    register_errors(app)
    register_request_handlers(app)
    register_logging(app)
    register_commands(app)
    with app.app_context():
        from src.apis.v1.system.userinfo import UserResource
        # Register the API documentation after routes are registered
   
        #docs.register(UserResource, blueprint='api_v1', endpoint='user_detail')
        
        #docs.register(UserResource,blueprint='api_v1', endpoint='user_create')
    # auth.init_app(app)

    return app

