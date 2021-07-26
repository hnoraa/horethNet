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

    # base routes
    @app.route('/')
    @app.route('/index')
    def index():
        print(request.headers)
        print(request)
        print(session)
        if request.headers.get('Authorization'):
            auth_header = request.headers.get('Authorization')
            access_token = auth_header.split(" ")[1]

            if access_token:
                user_id = User.decode_token(access_token)

                if not isinstance(user_id, str):
                    return render_template('index.html', title='Home', user=user_id)
                else:
                    # return render_template('index.html', title='Home', user=None)
                    return redirect(url_for('auth.login_view'))
        else:
            # return render_template('index.html', title='Home', user=None)
            print('user doesnt exist')
            return redirect(url_for('auth.login_view'))


    # import the login blueprint

    # import the auth blueprint
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
