from django.contrib import admin

from .models import Balance


class BalanceAdmin(admin.ModelAdmin):
    search_fields = ("user__name",)
    list_display = ("id", "user", "initial", "current", "total")
    autocomplete_fields = ("user",)


admin.site.register(Balance, BalanceAdmin)
