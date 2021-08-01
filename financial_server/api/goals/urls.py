from django.urls import path

from .views import EditGoal, Sync, Details, EditGoalSavingTransaction

app_name = "goals"

urlpatterns = [
    path('', Sync.as_view(), name="sync"),
    path('<int:id>', Details.as_view(), name="details"),
    path('edit-goal', EditGoal.as_view(), name="edit_goal"),
    path('edit-transaction', EditGoalSavingTransaction.as_view(), name="edit_goal_saving_transaction"),
]
