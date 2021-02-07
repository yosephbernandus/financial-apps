from functools import wraps
from typing import Callable, Any

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from dana_bagus_server.apps.permissions.constants import PermissionType


def has_permission(permission: PermissionType) -> Callable:
    """ Decorator to protect view for user that has the correct permission
        ex:

        from dana_bagus_server.apps.permissions.constants import PermissionType
        from dana_bagus_server.apps.permissions.decorators import has_permission

        @has_permission(PermissionType.VERIFY_USER)
        def verify_user(request):
            pass
    """

    def _permission_decorator(view_func: Callable) -> Callable:

        @wraps(view_func)
        def _check_user_account(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

            # Guard against not logged in
            if not request.user.is_authenticated:
                messages.info(request, 'Harap masuk terlebih dahulu.')
                return redirect_to_login(request.path_info)

            # Super user should bypass every check
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Actual Check for permissions
            has_permission = request.user.has_permission(permission)
            if has_permission:
                return view_func(request, *args, **kwargs)

            messages.info(request, 'Anda tidak memiliki izin yang benar untuk melakukan aksi ini.')

            # Try to login to refering page back, if not possible, redirect to login
            referrer = request.META.get('HTTP_REFERER')
            if referrer:
                return redirect(referrer)

            return redirect_to_login(request.path_info)

        return _check_user_account

    return _permission_decorator
