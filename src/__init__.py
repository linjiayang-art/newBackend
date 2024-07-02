from flask import Flask
from src.core.extensions import  db
from src.views.index import index_bp
from src.core.errors import register_errors
from src.core.request import register_request_handlers
from src.core.logging import register_logging
from src.core.commands import register_commands
from src.settings import config,basedir
import os
from src.apis import api_v1

def inin_flie():
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
    
    inin_flie()
    app.config.from_object(config[config_name])
    #extensions
    db.init_app(app)
    register_errors(app)
    register_request_handlers(app)
    register_logging(app)
    register_commands(app)
    # auth.init_app(app)

    return app

