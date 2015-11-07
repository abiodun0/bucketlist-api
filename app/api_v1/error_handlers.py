from flask import jsonify, request
from . import api

""" This files handles all the default http errors """

@api.app_errorhandler(404)
def page_not_found(e):
    """Decorated exception for non-existing url"""
    response = jsonify({'error': 'Page not found'})
    response.status_code = 404
    return response

@api.app_errorhandler(500)
def internal_server_error(e):
    """Decorated exception for internal server error"""

    response = jsonify({'error': 'internal server error'})
    response.status_code = 500
    return response

@api.app_errorhandler(400)
def bad_request(e):
    """Decorated exception for bad request"""
    response = jsonify({'error': 'bad request'})
    response.status_code = 400
    return response

@api.app_errorhandler(405)
def method_not_allowed(e):
    """Decorated exception for non-existing method on a route"""
    response = jsonify({'error': 'method not allowed'})
    response.status_code = 405
    return response