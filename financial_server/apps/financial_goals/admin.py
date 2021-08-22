from django.contrib import admin

from .models import FinancialGoal, GoalSavingsTransaction


class FinancialGoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'goal_name', 'amount', 'achievement_date')
    search_fields = ("goal_name", "user__name")
    autocomplete_fields = ("user",)


admin.site.register(FinancialGoal, FinancialGoalAdmin)
admin.site.register(GoalSavingsTransaction)
