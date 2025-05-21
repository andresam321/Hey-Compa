from flask import Blueprint, request
from app.models import User, db
from flask_login import current_user, login_user, logout_user, login_required

auth_routes = Blueprint('auth', __name__)


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': {'message': 'Unauthorized'}}, 401


@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return user.to_dict()

    return {'errors': {'message': 'Invalid credentials'}}, 401


@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'User logged out'}


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    data = request.get_json()

    required_fields = ['email', 'password', 'firstname', 'lastname']
    if not all(field in data for field in required_fields):
        return {'errors': {'message': 'Missing fields'}}, 400

    user = User(
        email=data['email'],
        password=data['password'],
        firstname=data['firstname'],
        lastname=data['lastname']
    )
    db.session.add(user)
    db.session.commit()
    login_user(user)

    return user.to_dict()


@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': {'message': 'Unauthorized'}}, 401