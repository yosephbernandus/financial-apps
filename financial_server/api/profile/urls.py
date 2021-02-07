from django.urls import path
from .views import HelloWorldView

app_name = "profile"

urlpatterns = [
    path('', HelloWorldView.as_view(), name="hello_world"),
]
