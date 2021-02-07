from typing import List, Any
from financial_server.core.utils import normalize_phone

from django import forms
from django.contrib import admin
from django.contrib.auth.forms import (UserChangeForm as DjangoUserChangeForm,
                                       UserCreationForm as DjangoUserCreationForm)
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.http import HttpRequest
from .models import User, Profile


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_phone(self) -> str:
        user_phone = normalize_phone(self.cleaned_data['phone'])

        if 'phone' in self.changed_data:
            if User.objects.filter(phone=user_phone).exists():
                raise forms.ValidationError("Telepon sudah terdaftar", code='duplicate_phone')

        return user_phone


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_email(self) -> str:
        user_email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=user_email).exists():
            raise forms.ValidationError("Surel sudah terdaftar", code='duplicate_email')

        return user_email

    def clean_phone(self) -> str:
        user_phone = normalize_phone(self.cleaned_data['phone'])

        if User.objects.filter(phone=user_phone).exists():
            raise forms.ValidationError("Nomor telepon sudah terdaftar", code='duplicate_phone')

        return user_phone

    def save(self, commit: bool = True, *args: Any, **kwargs: Any) -> User:
        user = super().save(*args, **kwargs)

        Profile.objects.create(
            user=user, birthday=user.date_joined, gender=Profile.GENDER.male,
            notes="Created from admin, please update the profile manually"
        )

        return user


class UserAdmin(DjangoUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    exclude = ('password',)
    search_fields = ('name', 'phone', 'email')
    list_display = ('id', 'name', 'phone', 'email')

    # Code belows must be add so it can adapts with DjangoUserAdmin interface
    ordering = ('id',)
    list_filter = ()

    def get_fieldsets(self, request: HttpRequest, obj=None) -> List:  # type: ignore
        return [(None, {'fields': self.get_fields(request, obj)})]


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__name',)
    autocomplete_fields = ("user",)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
