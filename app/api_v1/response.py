from flask import jsonify, request
from . import api

""" Handles the custom exception messages set at different poin of the app routes"""
def unauthorized(message):
    #handles unauthorized
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    #handle for forbidden item for a particular user
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

def notacceptable(message, email=" "):
    #handles the not acceptable method
    response = jsonify({'error': '{} {}'.format(email,message)})
    response.status_code = 406
    return response

def not_found(message, email=" "):
    #called when a resource cant be found
    response = jsonify({'error': '{} {}'.format(email,message)})
    response.status_code = 404
    return response

def custom_response(message, status_code):
    #handles other custom messages set throught out the api blue-print
    response = jsonify({'message': message})
    response.status_code = status_code
    return response
