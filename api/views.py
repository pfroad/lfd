# Create your views here.
import json

from django.http import HttpResponse


def login(request):
    result = {'status': False, 'data': None, 'error': None}
    # request.
    return HttpResponse(json.dumps(result, ensure_ascii=False))