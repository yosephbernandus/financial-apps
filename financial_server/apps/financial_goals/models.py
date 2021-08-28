from django.db import models
from django.utils import timezone

from model_utils import Choices


class FinancialGoal(models.Model):
    user = models.ForeignKey('users.User', related_name="financial_goals", on_delete=models.CASCADE)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    goal_name = models.CharField(blank=True, null=True, max_length=64)
    achievement_date = models.DateField(db_index=True, blank=True, null=True)
    CYCLE = Choices(
        (1, 'daily', 'Harian'),
        (2, 'weekly', 'Mingguan'),
        (3, 'monthly', 'Bulanan'),
        (4, 'yearly', 'Tahunan'),
    )
    deposit_cycle = models.PositiveSmallIntegerField(choices=CYCLE)
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return self.goal_name


class GoalSavingsTransaction(models.Model):
    goal = models.ForeignKey('financial_goals.FinancialGoal', related_name="transactions", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return f"{self.id}"
