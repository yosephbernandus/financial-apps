from django.urls import path

from .views import Sync, EditTransaction

app_name = "transactions"

urlpatterns = [
    path('', Sync.as_view(), name="sync"),
    path('edit-transaction', EditTransaction.as_view(), name="edit_transaction"),
]

