import datetime
import json
import random

import coreapi
import coreschema
# Create your views here.
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from frontend import common
from frontend.common import Result
from frontend.settings import DEBUG
from msg.models import SmsCode
from user.models import User


@api_view(['POST'])
@schema(AutoSchema(
    manual_fields=[
        coreapi.Field('data', location='body', schema=coreschema.Object(
            description='{"mobile": "176666622222","verify_code(optional)":"5462"}'
        ),
        required=True),
        # coreapi.Field('verifyCode', location='form', schema=coreschema.String(description='verifyCode(optional)'))
    ]
))
def sms_reg(request):
    data = request.data

    code = random.randint(100000, 999999)
    send_code(data["mobile"], code)

    if DEBUG:
        result = Result(data=code)
    else:
        result = Result()
    return Response(json.dumps(result))


@api_view(['POST'])
@schema(AutoSchema(
    manual_fields=[
        coreapi.Field('data', location='body', schema=coreschema.Object(
            description='{"mobile": "176666622222","verify_code(optional)":"5462"}'
        ),
        required=True),
    ]))
def sms_login(request):
    data = request.data

    user = User.objects.get(mobile=data["mobile"])

    if user == None:
        return Response(json.dumps(Result(status=common.USER_NOT_EXIST, error="用户不存在")))

    code = random.randint(100000, 999999)
    send_code(data["mobile"], code)

    if DEBUG:
        result = Result(data=code)
    else:
        result = Result()
    return Response(json.dumps(result))

def send_code(mobile, code):
    sms_code = SmsCode()
    sms_code.code = code
    sms_code.mobile = mobile
    sms_code.created_at = datetime.datetime.now()
    delta = datetime.timedelta(minutes=5)
    sms_code.expired_at = sms_code.created_at + delta

    sms_code.save()
