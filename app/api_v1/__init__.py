""" Initializes the flask blue print app withing the module"""
from flask import Blueprint

#this is set to a variable
api = Blueprint('api', __name__)

#Import all the neccesary files to be used for the application

from . import authentication, bucketlist, response, item, user, error_handlers, pagination