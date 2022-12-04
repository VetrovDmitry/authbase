from flask import Flask
from flask_restful import Api
from flask_apispec.extension import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from os import getenv
import logging

from .database import db, migrate
from .utils import read_api_config
from .config import CONFIGS


API_CONFIG = read_api_config()


def create_spec_and_doc(app):
    spec = APISpec(
        title=API_CONFIG["TITLE"],
        version=API_CONFIG["API_VERSION"],
        plugins=[MarshmallowPlugin()],
        openapi_version=API_CONFIG["OPENAPI_VERSION"]
    )
    app.config.update({
        "APISPEC_SPEC": spec,
        "APISPEC_SWAGGER_URL": API_CONFIG["SWAGGER_URL"],
        "APISPEC_SWAGGER_UI_URL": API_CONFIG["SWAGGER_UI_URL"]
    })

    api = Api(app, prefix='/api')
    docs = FlaskApiSpec(app)

    def add_component(component, component_route):
        api.add_resource(component, component_route)
        docs.register(component)

    return app


def create_app():
    app_config = CONFIGS.get(getenv('APP_MODE', 'dev'))

    flask_app = Flask(__name__)
    flask_app.config.from_object(app_config)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    mail.init_app(flask_app)