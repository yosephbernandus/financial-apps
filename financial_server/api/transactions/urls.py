from django.urls import path

from .views import Sync

app_name = "transactions"

urlpatterns = [
    path('', Sync.as_view(), name="sync"),
]

