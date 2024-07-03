from flask_sqlalchemy import SQLAlchemy
from src import flask_httpauth
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
db=SQLAlchemy()
spec = APISpec(
    title="User Info API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
# auth=flask_httpauth.HTTPBasicAuth()