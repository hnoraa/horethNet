import json
from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify, render_template, url_for, redirect
from app.models import User, BlacklistToken


class RegistrationView(MethodView):
    """This class registers a new user"""

    def post(self):
        """
        Handle a POST request for this view
        url: /auth/register
        """

        # query to see if user exists
        # user = User.query.filter_by(email=request.data['email']).filter_by(username=request.data['username']).first()
        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            # there is no user
            try:
                post_data = request.data

                # register the user
                email = post_data['email']
                username = post_data['username']
                firstName = post_data['firstName']
                lastName = post_data['lastName']
                password = post_data['password']

                # create the user and save
                user = User(email=email, username=username,
                            firstName=firstName, lastName=lastName, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }

                # return a 201 response
                return make_response(jsonify(response)), 201
            except Exception as e:
                # an error occured return error message
                response = {
                    'message': str(e)
                }

                return make_response(jsonify(response)), 401
        else:
            # the user already exists, cant create a user with the same email and username
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """Login views"""

    def post(self):
        """Attempt to login"""
        try:
            # check to see that the user exists
            # user = User.query.filter_by(email=request.data['email']).filter_by(username=request.data['username']).first()
            user = User.query.filter_by(
                username=request.data['username']).first()

            if user and user.password_is_valid(request.data['password']):
                # generate the access token which will be used as the authorization header
                access_token = user.generate_token(user.id)

                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token
                    }
                    # return make_response(jsonify(response)), 200
                    return redirect(url_for('index'))
            else:
                # user not found
                response = {
                    'message': 'Invalid email or password, Please try again'
                }

                return make_response(jsonify(response)), 401
        except Exception as e:
            # response to send error
            response = {
                'message': str(e)
            }

            # return 500 error (Internal Server Error)
            return make_response(jsonify(response)), 500


class LogoutView(MethodView):
    """Logout views"""

    def post(self):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            resp = User.decode_auth_token(access_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=access_token)
                try:
                    # insert the token
                    blacklist_token.save()

                    response = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(response)), 200
                except Exception as e:
                    response = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response)), 403


registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')

# define the routes
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=login_view,
    methods=['POST']
)
