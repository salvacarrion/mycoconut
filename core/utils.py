import json

from django.http import HttpResponse


def json_response(msg=None, error=False, data=None):
    res = {'error': error, 'message': msg, 'data': data}
    return HttpResponse(json.dumps(res), content_type='application/json')