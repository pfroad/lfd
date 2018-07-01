# Create your views here.
import datetime

import coreapi
import coreschema
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from django.db import transaction

from user.models import User


@api_view(['GET', 'POST'])
@schema(AutoSchema(
    manual_fields=[coreapi.Field('uid', location='query',  schema=coreschema.String(description='search value')),
                   coreapi.Field('page', location='query', schema=coreschema.Integer(description='page',)), ]))
def user_detail(request):
    """
    User detail
    """
    uid = request.query_params['uid']
    page = request.query_params['page']
    print(page)
    user = User.objects.filter(user_id=uid)
    return Response(user)

@api_view(['POST'])
@transaction.atomic
@schema(AutoSchema(
    manual_fields=[coreapi.Field('data', location='body', schema=coreschema.Object(description='{"uid":str, "page":int}')),]))
def register(request):
    """
    user register api
    :param request:
    :return:
    """
    mobile = request.data
    code = request.data

    user = User()
    user.mobile = mobile
    # datetime.datetime.now().date()
    user.birthday = datetime.datetime.now().date()

    # User.objects
    return Response({})