from flask_sqlalchemy import SQLAlchemy
from src import flask_httpauth
from flask_apispec import FlaskApiSpec
db=SQLAlchemy()
docs = FlaskApiSpec()
# auth=flask_httpauth.HTTPBasicAuth()