from django.db import models
from django.utils import timezone


class Balance(models.Model):

    user = models.OneToOneField('users.User', related_name='balance', on_delete=models.CASCADE)
    initial = models.FloatField()
    current = models.FloatField(default=0)
    total = models.FloatField(default=0)
    notes = models.TextField(default='')
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return f"Balance for user#{self.user.id}"
