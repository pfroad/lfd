import hashlib
import json
import random
import time

from django.http import HttpResponseBadRequest, HttpResponse

def encode_passwd(mobile, user_id, password):
    prefix = mobile[-4:]
    suffix = user_id[-8:-4]
    hash_md5 = hashlib.md5((prefix + password + suffix).encode('utf-8'))
    return hash_md5.hexdigest()

def gen_user_id(mobile):
    prefix = time.strftime("%y%m%d%H%M%S") + str(random.randint(10, 99))
    return prefix + mobile[-4:]

def check_required(required_params=None):
    def decorator(fn):
        def handler(request, *args, **kwds):
            print(required_params)
            data = request.data
            for required_param in required_params:
                if not required_param in data:
                    return HttpResponseBadRequest(
                        HttpResponse(json.dumps(
                            {'status': MISS_REQUIRED, 'data': None, 'error': "miss required param " + required_param})))
            return fn(request, *args, **kwds)
        return handler
    return decorator


class Result(json.JSONEncoder):
    def __init__(self, status=0, data=None, error=None):
        self.status = status
        self.data = data
        self.error = error

REQ_SUCCESS = 1000

USER_EXIST = 2000
USER_NOT_EXIST = 2001
USER_DISABLED = 2002
USER_PWD_ERR = 2003

MISS_REQUIRED = 2010

SMS_CODE_EXPIRED = 2050
# MISS_REQUIRED_ERROR = ""


if __name__ == '__main__':
    print(gen_user_id('17665418960'))
    print(encode_passwd('17665418960', gen_user_id('17665418960'), '123456'))