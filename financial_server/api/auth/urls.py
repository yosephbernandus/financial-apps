from django.urls import path

from .views import AuthLogin, Register, Logout, ChangePassword

app_name = "auth"

urlpatterns = [
    path('login', AuthLogin.as_view(), name="login"),
    path('register', Register.as_view(), name="register"),
    path('logout', Logout.as_view(), name="logout"),
    path('change-password', ChangePassword.as_view(), name="change-password"),
]
