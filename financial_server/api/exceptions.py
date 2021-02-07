import json

from django.utils import timezone
from django_redis import get_redis_connection

from rest_framework.views import exception_handler

from .utils import get_client_ip


class APIError(Exception):

    def __init__(self, status_code=None, detail=''):
        self.status_code = status_code
        self.detail = detail


def handle_exception(exc, context):
    request = context['request']

    # exception_handler will return None if status code is 500
    # ref: https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/views.py
    # func: exception_handler
    response = exception_handler(exc, context)

    if response:
        return response

    data = {
        'path': request.get_full_path(),
        'ip': get_client_ip(request),
        'response_status': 500,
        'time': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S'),
        'request_data': unicode(request.body, encoding='utf-8', errors='replace'),
        'response_data': {'error_description': str(exc)}
    }

    log_data = json.dumps(data)
    redis = get_redis_connection('log')
    key = 'log-500-errors:fail'

    with redis.pipeline() as pipeline:
        pipeline.lpush(key, log_data)
        pipeline.ltrim(key, 0, 99)
        pipeline.execute()

    return response
