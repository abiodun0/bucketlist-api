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

def notacceptable(message, email=" "):
    response = jsonify({'error': '{} {}'.format(email,message)})
    response.status_code = 406
    return response

def not_found(message, email=" "):
    response = jsonify({'error': '{} {}'.format(email,message)})
    response.status_code = 404
    return response

def created(message):
    response = jsonify({'status': 'created','message': message})
    response.status_code = 201
    return response

def updated(message):
    response = jsonify({'status': 'updated','message': message})
    response.status_code = 200
    return response

def deleted(message):
    response = jsonify({'status': 'updated','message': message})
    response.status_code = 204
    return response