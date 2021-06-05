from django import forms

from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta

from financial_server.constants import PROVINCES
from financial_server.core.fields import MobilePhoneField

from django.utils import timezone

from financial_server.apps.users.models import User, Profile
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
            raise forms.ValidationError("Pengguna dengan email ini tidak ada")

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
                'Harap masukkan email dan kata sandi yang benar.'
            )

        self.user_cache = self.user
        self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegistrationForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    nik = forms.CharField()
    phone = MobilePhoneField()
    address = forms.CharField()
    birthday = forms.CharField()
    gender = forms.ChoiceField(choices=Profile.GENDER)
    password = forms.CharField()

    def clean_email(self) -> str:
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Pengguna dengan email ini sudah ada',
                                        code='duplicate_email')
        return email

    def clean_phone(self) -> str:
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Pengguna dengan nomor telepon ini sudah ada')
        return phone

    def clean_birthday(self) -> date:
        birthday = self.cleaned_data.get('birthday')

        try:
            birthday = parser.parse(birthday).date()
        except ValueError:
            raise forms.ValidationError("%s bukan format yang benar" % birthday)

        if birthday > timezone.now().date() - relativedelta(years=17):
            raise forms.ValidationError("Usia minimum adalah 17 tahun")

        if birthday.year < 1900:
            raise forms.ValidationError("Ulang tahun tidak bisa didaftarkan")

        return birthday

    def clean_nik(self) -> str:
        """ Determine province from NIK prefix
        """
        nik = self.cleaned_data['nik']
        province_code = int(nik[:2])
        valid_province = set([province[0] for province in PROVINCES])
        if (len(nik) != 16):
            raise forms.ValidationError("NIK harus 16 karakter")
        if province_code not in valid_province:
            raise forms.ValidationError("Nomor NIK tidak valid")
        if User.objects.filter(nik=nik).exists():
            raise forms.ValidationError('Pengguna dengan nik ini sudah ada')
        return nik

    def save(self) -> User:
        nik = self.cleaned_data['nik']
        address = self.cleaned_data['address']

        user: User = User.objects.create(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            nik=nik,
            phone=self.cleaned_data['phone'],
            province=nik[:2] if nik else None,
        )

        Profile.objects.create(
            user=user,
            address=address,
            birthday=self.cleaned_data['birthday'],
            gender=self.cleaned_data['gender'],
        )
        return user
