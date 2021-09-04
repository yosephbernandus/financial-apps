import math

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

    def deposit_amount_per_cycle(self) -> float:
        if not self.achievement_date:
            raise ValueError('Invalid achievement date')

        days = (self.achievement_date - self.created.date()).days
        if self.deposit_cycle == FinancialGoal.CYCLE.daily:
            deposit_amount = self.amount / days
        elif self.deposit_cycle == FinancialGoal.CYCLE.weekly:
            avg_amount = self.amount / math.ceil(days / 7)
            deposit_amount = math.ceil(avg_amount)
        elif self.deposit_cycle == FinancialGoal.CYCLE.monthly:
            avg_amount = self.amount / math.ceil(days / 30)
            deposit_amount = math.ceil(avg_amount)
        else:
            avg_amount = self.amount / math.ceil(days / 365)
            deposit_amount = math.ceil(avg_amount)

        return deposit_amount


class GoalSavingsTransaction(models.Model):
    goal = models.ForeignKey('financial_goals.FinancialGoal', related_name="transactions", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return f"{self.id}"
