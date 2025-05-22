from flask import Blueprint, request, jsonify, abort
from app.models import User, db
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, SignUpForm
from flask_wtf.csrf import generate_csrf

auth_routes = Blueprint('auth', __name__)


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': {'message': 'Unauthorized'}}, 401

@auth_routes.route('/csrf/reset', methods=['POST'])
def reset_csrf():
    """
    Resets the CSRF token.
    """
    # This route is used to reset the CSRF token
    # when the user logs in or signs up.
    # It is not used in the frontend.
    return {'csrf_token': generate_csrf()}

@auth_routes.route('/csrf/restore', methods=['GET'])
def restore_csrf():
    response = jsonify({'message': 'CSRF cookie set'})
    response.set_cookie('csrf_token', generate_csrf())
    return response

@auth_routes.route('/csrf/verify', methods=['POST'])
def verify_csrf():
    """
    Verifies the CSRF token.
    """
    # This route is used to verify the CSRF token
    # when the user logs in or signs up.
    # It is not used in the frontend.
    return {'csrf_token': generate_csrf()}

@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    print("Login route hit ✅")
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    print("incoming Email:", request.form.get('email'))
    print("incoming Password:", request.form.get('password'))
    print("incoming CSRF Token:", request.cookies.get('csrf_token'))
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        # Add the user to the session, we are logged in!
        user = User.query.filter(User.email == form.data['email']).first()

        login_user(user)
        return user.to_dict()
    return form.errors, 401



@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'User logged out'}


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password'],
            firstname=form.data['firstname'],
            lastname=form.data['lastname']
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return user.to_dict()
    return form.errors, 401



@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': {'message': 'Unauthorized'}}, 401