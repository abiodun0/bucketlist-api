from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    """ 
    A utility function that initializes creation of the api app
    """

    app = Flask(__name__)

    current_config = config[config_name]

    app.config.from_object(current_config)

    db.init_app(app)

    from .api_v1 import api
    #prefixes all the url with /api/v1/
    app.register_blueprint(api, url_prefix='/api/v1')

    return app
