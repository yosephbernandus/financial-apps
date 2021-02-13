from django.contrib import admin

from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    search_fields = ("user__name",)
    list_display = ("id", "user", "amount", "type", "created")
    autocomplete_fields = ("user",)


admin.site.register(Transaction, TransactionAdmin)
