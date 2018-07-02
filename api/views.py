# Create your views here.
import random

import coreapi
import coreschema
from rest_framework.decorators import api_view, schema
from django.db import transaction
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema


@api_view(['POST'])
@schema(AutoSchema(
    manual_fields=[
        coreapi.Field('mobile', location='body', schema=coreschema.String(description='mobile(Reqiured)'), required=True),
        # coreapi.Field('verifyCode', location='body', schema=coreschema.String(description='verifyCode(optional)'))
    ]
))
def sms_code(request):
    code = random.randint(100000, 999999)
    transaction.on_commit()
    return Response({})