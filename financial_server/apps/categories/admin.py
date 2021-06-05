from django.contrib import admin

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


admin.site.register(Category, CategoryAdmin)
