from django.urls import path

from .views import AuthLogin, Register

app_name = "auth"

urlpatterns = [
    path('login', AuthLogin.as_view(), name="login"),
    path('register', Register.as_view(), name="register"),
]
