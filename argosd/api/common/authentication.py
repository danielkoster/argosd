import logging

from functools import wraps
from flask import request, Response

from argosd import settings


def check_authentication(secret):
    return secret == settings.API_TOKEN

def authenticate():
    """Sends a 401 response"""
    return Response('You have to login with proper credentials', 401)

def requires_authentication(function):
    """Creates a method that can be used with @requires_authentication
    to protect an API endpoint"""
    @wraps(function)
    def decorated(*args, **kwargs):
        secret = request.headers['X-Api-Token'] if \
            'X-Api-Token' in request.headers else None

        if not check_authentication(secret):
            return authenticate()
        return function(*args, **kwargs)
    return decorated
