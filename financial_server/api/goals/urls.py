from django.urls import path

from .views import Sync

app_name = "goals"

urlpatterns = [
    path('', Sync.as_view(), name="sync"),
]
