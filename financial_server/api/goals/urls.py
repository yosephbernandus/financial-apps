from django.urls import path

from .views import Sync, Details

app_name = "goals"

urlpatterns = [
    path('', Sync.as_view(), name="sync"),
    path('<int:id>', Details.as_view(), name="details"),
]
