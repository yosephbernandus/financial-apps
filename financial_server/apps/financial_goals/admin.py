from django.contrib import admin

from .models import FinancialGoal, GoalSavingsTransaction


class FinancialGoalAdmin(admin.ModelAdmin):
    search_fields = ("goal_name", "user__name")
    autocomplete_fields = ("user",)


admin.site.register(FinancialGoal, FinancialGoalAdmin)
admin.site.register(GoalSavingsTransaction)
