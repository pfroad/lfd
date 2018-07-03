# Create your views here.
import datetime
import json

import coreapi
import coreschema
from django.db import transaction
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from frontend import common
from frontend.common import check_required, Result, encode_passwd, gen_user_id
from frontend.models import SmsCode, User


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
    user = User.objects.filter(user_id=uid).first()
    return Response(user)

@api_view(['POST'])
@transaction.atomic
@schema(AutoSchema(
    manual_fields=[
        coreapi.Field('data', location='body', schema=coreschema.Object(
            description='{"mobile":"18665411234", "password":"123456", "verify_code":"123456"}'
        ), required=True),
    ]))
@check_required(["mobile", "password", "verify_code"])
def register(request):
    """
    user register api
    :param request:
    :return:
    """
    data = request.data
    mobile = data["mobile"]
    code = data["verify_code"]
    password = data["password"]
    #
    # sms_code = SmsCode.objects.filter(code=code).first()
    #
    # expired_date = sms_code.expired_date
    now = datetime.datetime.now()
    # # delta = datetime.timedelta(minutes=5)
    # if sms_code.verified > 0 or expired_date < now:

    res = SmsCode.objects.filter(code=code, mobile=mobile, expired_date__lt=now).update(verified=1)

    if res == 0:
        return Response(json.dumps(Result(status=common.SMS_CODE_EXPIRED, error="code has been expired")))

    user = User()
    user.user_id = gen_user_id(mobile)
    user.mobile = mobile
    user.password = encode_passwd(mobile, user.user_id, password)
    # datetime.datetime.now().date()
    user.birthday = datetime.datetime.now().date()
    user.created_at = datetime.datetime.now()
    user.save()

    # User.objects
    return Response({})

@api_view(['POST'])
@transaction.atomic
@schema(AutoSchema(
    manual_fields=[
        coreapi.Field('data', location='body', schema=coreschema.Object(
            description='{"mobile":"18665411234", "password":"123456"}'
        ), required=True),
    ]))
@check_required(["mobile", "password"])
def passwd_login(request):
    data = request.data

    mobile = data["mobile"]
    password = data["password"]

    user = User.objects.get(mobile=mobile, is_deleted=0)

    if user == None:
        return Response(json.dumps(Result(status=common.USER_NOT_EXIST, error="用户不存在")))
    elif user.is_disabled:
        return Response(json.dumps(Result(status=common.USER_DISABLED, error="账户被冻结")))

    passwd = encode_passwd(mobile, user.user_id, password)

    if password != passwd:
        return Response(json.dumps(Result(status=common.USER_PWD_ERR, error="密码错误")))



# @api_view(['POST'])
# @transaction.atomic
# @schema(AutoSchema(
#     manual_fields=[
#         coreapi.Field('mobile', location='form', schema=coreschema.Object(description='mobile'), required=True),
#         coreapi.Field('password', location='form', schema=coreschema.Object(description='password'), required=True),
#     ]))
# def register(request):
#     """
#     user register api
#     :param request:
#     :return:
#     """
#     data = json.loads(request.data)
#     mobile = data["mobile"]
#     code = data[""]
#
#     user = User()
#     user.mobile = mobile
#     # datetime.datetime.now().date()
#     user.birthday = datetime.datetime.now().date()
#     user.created_date = datetime.datetime.now()
#
#     # User.objects
#     return Response({})