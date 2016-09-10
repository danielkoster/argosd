from functools import wraps
from flask import request, Response

from argosd import settings


def check_authentication(username, token):
    return username == 'argosd' and token == settings.API_TOKEN


def authenticate():
    """Sends a 401 Unauthorized response that enables Basic Auth"""
    return Response('You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_authentication(function):
    """Creates a decorator that can be applied with @requires_authentication
    to protect an API endpoint"""
    @wraps(function)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_authentication(auth.username, auth.password):
            return authenticate()
        return function(*args, **kwargs)
    return decorated
