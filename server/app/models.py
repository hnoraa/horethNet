import jwt
import time
from app import db
from flask import current_app
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta


class User(db.Model):
    """The user class"""
    __tablename__ = 'users'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    firstName = db.Column(db.String(256))
    lastName = db.Column(db.String(256))

    # foreign key relationships

    # methods
    def __init__(self, email, username, firstName, lastName, password):
        """Initialize the user"""
        self.email = email
        if len(username) == 0:
            self.username = email
        else:
            self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """Check the password against the users password hash"""
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save the user to the database"""
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """Generate the access token given the user id"""
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            # create the byte string token using the payload and the SECRET key (from environment)
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )

            return jwt_string
        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header"""
        try:
            # try to decode the token using the SECRET key (from environment)
            payload = jwt.decode(token, current_app.config.get(
                'SECRET'), algorithms=['HS256'])

            # return the user id after successfully decoding the token
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired token. Please login to get a new token.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please register or login.'


class BlacklistToken(db.Model):
    """Stores JWT tokens"""
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    def save(self):
        """Save the token to the database"""
        db.session.add(self)
        db.session.commit()
