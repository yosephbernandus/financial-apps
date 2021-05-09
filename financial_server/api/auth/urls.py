from django.urls import path

from .views import AuthLogin

app_name = "auth"

urlpatterns = [
    path('login', AuthLogin.as_view(), name="login"),
]
