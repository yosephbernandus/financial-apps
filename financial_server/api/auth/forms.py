from django import forms

from financial_server.apps.users.models import User
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm

from typing import Dict, Any


class AuthenticationForm(DjangoAuthForm):
    username = forms.CharField()
    password = forms.CharField()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean_username(self) -> str:
        username = self.cleaned_data['username'].strip().lower()

        self.user = User.objects.filter(email=username).first()
        if not self.user:
            raise forms.ValidationError("Pengguna dengan email / nomor ponsel ini tidak ada")

        return username

    def clean(self) -> Dict:
        """ Copy pasted from django core,
            basically change the authenticate signature to use identifier-password
        """

        if self.errors:
            return self.cleaned_data

        assert self.user is not None
        if not self.user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError(
                'Harap masukkan email / nomor ponsel dan kata sandi yang benar.'
            )

        self.user_cache = self.user
        self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
