import datetime
import json
import random

import coreapi
import coreschema
from django.db import transaction
# Create your views here.
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from frontend.common import Result
from frontend.settings import DEBUG
from msg.models import SmsCode
from user.models import User


@api_view(['POST'])
@schema(AutoSchema(
    manual_fields=[
        coreapi.Field('data', location='body', schema=coreschema.String(description='{"mobile": "176666622222"}, "verifyCode": "5462(optional)"'), required=True),
        # coreapi.Field('verifyCode', location='form', schema=coreschema.String(description='verifyCode(optional)'))
    ]
))
def sms_reg(request):
    data = json.loads(request.data)
    code = random.randint(100000, 999999)
    # transaction.on_commit()

    sms_code = SmsCode()
    sms_code.code = code
    sms_code.mobile = data["mobile"]
    sms_code.created_date = datetime.datetime.now()
    delta = datetime.timedelta(minutes=5)
    sms_code.expired_date = sms_code.created_date + delta

    sms_code.save()

    if DEBUG:
        result = Result(data=code)
    else:
        result = Result()
    return Response(json.dumps(result))

def sms_login(request):
    user = User.objects.filter(mobile=request.data)