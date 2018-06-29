import coreapi
import coreschema
from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema


@api_view(['POST'])
@schema(AutoSchema(
    manual_fields=[
        coreapi.Field(name="mobile",
                      required=True,
                      location="body",
                      schema=coreschema.String(description="sms mobile num")),
    ]
))
def sendCode(request):
    """

    :param request:
    :return:
    """
    pass