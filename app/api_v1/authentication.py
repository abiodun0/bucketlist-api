from flask import g, jsonify,request, current_app, url_for
from flask.ext.httpauth import HTTPBasicAuth
from .response import unauthorized, forbidden
from . import api
from ..models import User


#initializes the HTTPBasic auth library to be used for regular authenticaiton
auth = HTTPBasicAuth()


#Login Error Handler
@auth.error_handler
def auth_error():
    """Decorator function for login failed attempt"""
    return unauthorized("Invalid Credentials")

#login authenticaiton verifier
@auth.verify_password
def verify_password(email_or_token, password):
    """ Handles the login/token verificaiton
    @params email/token, optional password
    @sets global user object
    @returns Bool True/False

    """
    #checks if the password is empty
    if password is '':

        #get the user with the assigned token and store it in the global variable object
		g.current_user = User.verify_auth_token(email_or_token) 

        #returns true if it's verified succesfully
		return g.current_user is not None

    #checks for the email and returns false if not avaible
    user = User.query.filter_by(email=email_or_token).first() 
    if not user:
		return False
    g.current_user = user
    return user.verify_password(password)

 #Login endpoint
@api.route('/auth/login/', methods=['POST'])
def login():
    """ Logs in A user """
    email = request.json.get('email')
    password = request.json.get('password')

    # verifies and returns a token for the user
    if not verify_password(email, password):
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
    return response


def get_auth_token():
    """ Utility funciton to generate authentication token
    @params None
    @return token
    """
    token = g.current_user.generate_auth_token()
    return token.decode('ascii')
