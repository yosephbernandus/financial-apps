from django.db import models


class PermissionGroup(models.Model):
    name = models.CharField(
        max_length=50,
        help_text="Grouping for permission, only for UI. Ex: (User)"
    )

    def __str__(self) -> str:
        return f"PermissionGroup#{self.id}: {self.name}"


class Permission(models.Model):
    name = models.CharField(max_length=50, help_text="Ex: (Approve)")
    group = models.ForeignKey('permissions.PermissionGroup', related_name='permissions', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Permission#{self.id}: {self.name}"
