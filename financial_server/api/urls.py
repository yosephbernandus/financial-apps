from django.conf.urls import include
from django.urls import path

app_name = "api"

urlpatterns = [
    path('auth/', include('financial_server.api.auth.urls', namespace='auth')),
]
