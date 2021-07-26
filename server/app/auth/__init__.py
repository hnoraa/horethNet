from flask import Blueprint

# this instance of a Blueprint represents the auth blueprint
auth_blueprint = Blueprint('auth', __name__)

from . import views