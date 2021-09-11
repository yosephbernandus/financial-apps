from django import forms

from typing import Dict, Any

from financial_server.apps.users.models import User
from financial_server.apps.categories.models import Category
from financial_server.apps.transactions.models import Transaction


class EditTransactionForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    amount = forms.IntegerField()
    name = forms.CharField()
    type = forms.IntegerField()
    notes = forms.CharField(required=False)

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self) -> Dict:
        if self.errors:
            return self.cleaned_data

        name = self.cleaned_data['name']
        amount = self.cleaned_data['amount']
        type  = self.cleaned_data['type']

        if not name:
            raise forms.ValidationError("name cannot be empty")

        if float(amount) < 0.0:
            raise forms.ValidationError("amount cannot be less than 0")

        if int(type) == 0:
            raise forms.ValidationError("invalid type")

        return self.cleaned_data

    def save(self) -> Transaction:
        transaction = self.user.transactions.create(
            name=self.cleaned_data['name'],
            category=self.cleaned_data['categoty'],
            amount=self.cleaned_data['amount'],
            type=self.cleaned_data['type'],
            notes=self.cleaned_data['notes']
        )

        return transaction
