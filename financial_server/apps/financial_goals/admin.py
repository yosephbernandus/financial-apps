from django.contrib import admin

from .models import FinancialGoal


class FinancialGoalAdmin(admin.ModelAdmin):
    search_fields = ("goal_name", "user__name")
    autocomplete_fields = ("user",)


admin.site.register(FinancialGoal, FinancialGoalAdmin)
