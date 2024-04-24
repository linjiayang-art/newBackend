from flask import Flask
from src.core.extensions import  db,auth
from src.core.errors import register_errors
from src.core.request import register_request_handlers
from src.settings import config


import os
basedir=os.path.abspath(os.path.dirname(__file__))
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
    app=Flask('backend')
    inin_flie()
    app.config.from_object(config[config_name])
    #extensions
    db.init_app(app)
    register_errors(app)
    register_request_handlers(app)
    # auth.init_app(app)

    return app

