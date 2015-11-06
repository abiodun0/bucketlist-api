from flask import g, jsonify,request, current_app, url_for
from flask.ext.httpauth import HTTPBasicAuth
from .response import unauthorized, forbidden
from . import api
from ..models import User

auth = HTTPBasicAuth()


@auth.error_handler
def auth_error():
	return unauthorized("Invalid Credentials")

@auth.verify_password
def verify_password(email_or_token, password):
	if password is '':
		g.current_user = User.verify_auth_token(email_or_token) 
		g.token_used = True
		return g.current_user is not None
	user = User.query.filter_by(email=email_or_token).first() 
	if not user:
		return False
	g.current_user = user
	g.token_used = False
	return user.verify_password(password)


@api.route('/auth/login/', methods=['POST'])
def login():
    '''Logins a user'''
    email = request.json.get('email')
    password = request.json.get('password')

    # verifies and returns a token for the user
    if not verify_password(email,password):
    	return unauthorized("Wrong combination of email and password")

    token = get_auth_token()

    response = jsonify({'token': token, 'message': 'successfully logged in'})
    response.status_code = 200
    return response

# logout endpoint
@api.route('/auth/logout/', methods=['POST'])
@auth.login_required
def logout():

    response = jsonify({'status': 'Logged Out'})
    response.status_code = 201
    return repsonse


def get_auth_token():
    '''Generates a token'''
    token = g.current_user.generate_auth_token()
    return token.decode('ascii')
