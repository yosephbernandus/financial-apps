from django.urls import path

from .views import Sync, Details, AddSavingsTransaction

app_name = "goals"

urlpatterns = [
    path('', Sync.as_view(), name="sync"),
    path('<int:id>', Details.as_view(), name="details"),
    path('add-transaction', AddSavingsTransaction.as_view(), name="add_savings_transaction"),
]
