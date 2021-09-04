from django import forms
from django.utils import timezone

from dateutil import parser
from typing import Dict, Any

from financial_server.apps.users.models import User
from financial_server.apps.categories.models import Category
from financial_server.apps.financial_goals.models import FinancialGoal, GoalSavingsTransaction


class EditGoalForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    amount = forms.IntegerField()
    name = forms.CharField()
    achievement_date = forms.CharField()
    deposit_cycle = forms.IntegerField()

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self) -> Dict:
        if self.errors:
            return self.cleaned_data

        amount = self.cleaned_data['amount']
        name = self.cleaned_data['name']
        achievement_date = self.cleaned_data['achievement_date']

        try:
            achievement_date = parser.parse(achievement_date).date()
        except ValueError:
            raise forms.ValidationError("%s bukan format yang benar" % achievement_date)

        if achievement_date < timezone.localdate():
            raise forms.ValidationError("date of achievement of funds can not be less than today")

        if amount < 0:
            raise forms.ValidationError("amount cannot be less than 0")

        if not name:
            raise forms.ValidationError("name cannot be empty")

        return self.cleaned_data

    def save(self) -> FinancialGoal:
        goal = self.user.financial_goals.create(
            category=self.cleaned_data['category'],
            amount=self.cleaned_data['amount'],
            goal_name=self.cleaned_data['name'],
            achievement_date=parser.parse(self.cleaned_data['achievement_date']).date(),
            deposit_cycle=self.cleaned_data['deposit_cycle']
        )

        return goal


class EditGoalSavingTransactionForm(forms.Form):
    goal = forms.ModelChoiceField(queryset=FinancialGoal.objects.all())
    amount = forms.IntegerField()

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self) -> Dict:
        if self.errors:
            return self.cleaned_data

        if self.cleaned_data['goal'].user != self.user:
            raise forms.ValidationError("Not authorized user")

        return self.cleaned_data

    def save(self) -> GoalSavingsTransaction:
        goal = self.cleaned_data['goal']
        transaction = goal.transactions.create(
            amount=self.cleaned_data['amount']
        )

        return transaction
