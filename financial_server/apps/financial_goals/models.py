from django.db import models

from model_utils import Choices


class FinancialGoal(models.Model):
    user = models.ForeignKey('users.User', related_name="financial_goals", on_delete=models.CASCADE)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    amount = models.IntegerField()
    goal_name = models.CharField(blank=True, null=True, max_length=64)
    achievement_date = models.DateField(db_index=True, blank=True, null=True)
    CYCLE = Choices(
        (1, 'daily', 'Harian'),
        (2, 'weekly', 'Mingguan'),
        (3, 'monthly', 'Bulanan'),
        (4, 'yearly', 'Tahunan'),
    )
    deposit_cycle = models.PositiveSmallIntegerField(choices=CYCLE)

    def __str__(self) -> str:
        return self.goal_name
