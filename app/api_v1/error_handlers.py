from flask import jsonify, request
from . import api

@api.app_errorhandler(404)
def page_not_found(e):
    print e
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Page not found'})
        response.status_code = 404
        return response

@api.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response

@api.app_errorhandler(400)
def bad_request(e):
    response = jsonify({'error': 'bad request'})
    response.status_code = 400
    return response

@api.app_errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'error': 'method not allowed'})
    response.status_code = 405
    return response