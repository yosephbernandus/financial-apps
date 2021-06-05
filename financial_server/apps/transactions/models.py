from django.db import models
from django.utils import timezone
from django.db.models.enums import IntegerChoices

from financial_server.core.utils import FilenameGenerator

from thumbnails.fields import ImageField


class Transaction(models.Model):

    user = models.OneToOneField('users.User', related_name='transaction', on_delete=models.CASCADE)
    balance = models.ForeignKey('balances.Balance', related_name='transactions',
                                on_delete=models.CASCADE)

    class TYPE(IntegerChoices):
        income = 1, ('Income')
        outcome = 2, ('Outcome')

    type = models.PositiveSmallIntegerField(choices=TYPE.choices)
    amount = models.FloatField()
    notes = models.TextField(default='', blank=True, null=True)
    photo = ImageField(upload_to=FilenameGenerator(prefix='transactions'),
                       blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.localtime)

    def __str__(self) -> str:
        return f"Balance for user#{self.user.id}"