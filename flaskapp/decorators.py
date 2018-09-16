import json
from flask import Response
from functools import wraps


def json_response(func):
    @wraps(func)
    def cust_json_wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        return Response(response=json.dumps(data).encode('utf-8'), status=200, mimetype='x-application\json')
    return cust_json_wrapper


def connection_wrapper(func):
    @wraps(func)
    def conn_wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionRefusedError:
            return {'error': True, 'error_data': 'TCP connection refused'}
    return conn_wrap