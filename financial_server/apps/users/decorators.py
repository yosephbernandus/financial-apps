from functools import wraps
from typing import Callable, Any

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest, HttpResponse


def superuser_required(view_func: Callable) -> Callable:
    def _check_superuser(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated or not request.user.is_superuser:
            message = "Mohon masuk sebagai pengguna yang memiliki izin untuk dapat mengakses halaman ini"
            messages.info(request, message)
            return redirect_to_login(request.path_info)
        return view_func(request, *args, **kwargs)
    return wraps(view_func)(_check_superuser)
