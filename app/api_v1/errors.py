from flask import jsonify, request
from . import api

def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

def notacceptable(message, email=None):
    response = jsonify({'error': '{} {}'.format(email,message)})
    response.status_code = 406
    return response