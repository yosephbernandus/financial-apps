import json
import random
import time

from django.conf import settings
from django.contrib.auth import login

from django_redis import get_redis_connection

from rest_framework import status


def get_client_ip(request):
    """ Modified from http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django """
    cf_original_ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if cf_original_ip:
        return cf_original_ip

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # Get the last IP in http_x_forwarded_for http://en.wikipedia.org/wiki/X-Forwarded-For#Format
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_cache_key(token):
    key = 'api-auth:%s' % token
    return key


def force_login(request, user):
    """
    user should has backend attribute to login
    """
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
