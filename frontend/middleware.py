# coding=utf-8
import hmac
import json

from django.http import HttpResponseBadRequest, HttpResponse

from api.models import SecretKey

class VerifyRequestMiddleware(object):
    # def __init__(self):

    def __init__(self, get_response):
        self.get_response = get_response
        # print("Load keys")
        keys = list(SecretKey.objects.filter(enabled=1))
        self.keys_map = {}
        for key in keys:
            self.keys_map[key.app_id] = key.s_key

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        uri = request.path

        if uri.startswith("/api"):
            if request.method == 'POST':
                body = request.body
                if len(body) == 0:
                    return HttpResponseBadRequest(
                        HttpResponse(
                            json.dumps(
                                {'status': False, 'data': None, 'error': "request body is blank"})))

                data = json.loads((body).decode('utf-8'))
            elif request.method == 'GET':
                data = request.GET

            err = self.verify_require(data)
            if not err is None:
                return err

            sign = self.sign(data)
            if sign != data["sign"]:
                return HttpResponseBadRequest(
                    HttpResponse(
                        json.dumps(
                            {'status': False, 'data': None, 'error': "Cannot verify sign"})))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def verify_require(self, data):
        miss_key = None
        if not "app_id" in data:
            miss_key = "app_id"

        if not "sign" in data:
            miss_key = "sign"

        if not "timestamp" in data:
            miss_key = "timestamp"

        if not miss_key is None:
            return HttpResponseBadRequest(
                HttpResponse(
                    json.dumps({'status': False, 'data': None, 'error': "missing require parameter: {}".format(miss_key)})))

        return None

    def create_link_str(self, parameters):
        # paramKeys = parameters.keys()
        # paramKeys.sort()
        link_str = ""
        for key in sorted(parameters.keys()):
        # for i in range(len(paramKeys)):
        #     key = paramKeys[i]
            if key == "sign":
                continue

            link_str += key
            link_str += "="
            link_str += str(parameters[key])
            link_str += "&"
        return link_str[:-1]

    def sign(self, data):
        # print(self.api_secret_key)
        app_id = data["app_id"]
        if not app_id in self.keys_map:
            self.load_skey()
            if not app_id in self.keys_map:
                return False

        # secret_key = self.keys_map[app_id]
        myhmac = hmac.new(bytes(self.keys_map[app_id], "utf-8"))
        print(self.create_link_str(data))
        myhmac.update(bytes(self.create_link_str(data), "utf-8"))
        # print(myhmac.hexdigest())
        return myhmac.hexdigest()

    def load_skey(self):
        keys = list(SecretKey.objects.filter(enabled=1))
        self.keys_map = {}
        for key in keys:
            self.keys_map[key.app_id] = key.s_key