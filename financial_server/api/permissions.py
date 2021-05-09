from django.conf import settings

from rest_framework import status
from rest_framework.permissions import BasePermission

from .exceptions import APIError


class IsSecure(BasePermission):
    """
    Allows access only to secured request (HTTPS).
    """
    def has_permission(self, request, view):
        if not settings.DEBUG and not request.is_secure():
            raise APIError(status_code=status.HTTP_403_FORBIDDEN,
                           detail="Koneksi HTTPS diperlukan")
        return True
