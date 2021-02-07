from django.contrib import admin

from .models import PermissionGroup, Permission

admin.site.register(PermissionGroup)
admin.site.register(Permission)
