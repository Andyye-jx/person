import time
from functools import wraps
from flask_restful import Api as _Api
from flask_restful.utils import unpack
from werkzeug.exceptions import BadRequest, MethodNotAllowed
from werkzeug.wrappers import Response
from sqlalchemy.util import NoneType
from utils.error import error_code
from utils.exceptions import BadParameter, APIException


class Api(_Api):

    def handle_error(self, e):
        if isinstance(e, MethodNotAllowed):
            return self.make_response({
                'code': 'Method_Not_Allowed'
            }, 405)

        if isinstance(e, APIException):
            error = e
            msg = error_code.get(error, '')
        elif isinstance(e, BadRequest):
            error = 10002
            msg = e.data['message']
        elif isinstance(e, BadParameter):
            error = 10001
            msg = error_code.get(error, '')
        else:
            error = 10000
            msg = error_code.get(error, '')
        return self.make_response({
            "ret": error,
            "ts": int(time.time()),
            "msg": msg
        }, 200)

    def output(self, resource):

        @wraps(resource)
        def wrapper(*args, **kwargs):
            resp = resource(*args, **kwargs)
            if isinstance(resp, Response):
                return resp
            ori_data, code, headers = unpack(resp)
            data = {'ret': 200, "ts": int(time.time())}
            if isinstance(ori_data, dict) or isinstance(ori_data, list):
                data['data'] = ori_data
            elif isinstance(ori_data, NoneType):
                pass
            else:
                data['data'] = ori_data

            return self.make_response(data, 200, headers=headers)

        return wrapper
