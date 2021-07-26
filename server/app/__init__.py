from os import access
from flask import request, jsonify, abort, render_template, redirect, session
from flask.helpers import make_response, url_for
from flask_api import FlaskAPI
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config

# initialize SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    """
        Wrapper to create a new Flask object
        config_name: the configuration name (ie: 'dev', 'test', 'stage', 'prod')
    """
    # include the models
    from app.models import User

    app = FlaskAPI(__name__, instance_relative_config=True)

    # get the appropriate config from the app_config object
    app.config.from_object(app_config[config_name])

    # get appropriate config from config.py
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initlaize database and migrations
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)
    db.create_all()

    # tester route
    @app.route('/test', methods=['GET'])
    def test():
        return 'hello'

    # import the auth blueprint
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
