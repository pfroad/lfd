import datetime
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


@api_view(['POST'])
@schema(AutoSchema(
    manual_fields=[
        coreapi.Field('mobile', location='body', schema=coreschema.String(description='mobile(Reqiured)'), required=True),
        coreapi.Field('verifyCode', location='body', schema=coreschema.String(description='verifyCode(optional)'))
    ]
))
def sms_code(request):
    mobile = request.data
    code = random.randint(100000, 999999)
    transaction.on_commit()

    sms_code = SmsCode()
    sms_code.code = code
    sms_code.mobile = mobile
    delta = datetime.timedelta(minutes=5)
    sms_code.expired_date = datetime.datetime.now() + delta

    if DEBUG:
        result = Result(data=code)
    else:
        result = Result()
    return Response(result)