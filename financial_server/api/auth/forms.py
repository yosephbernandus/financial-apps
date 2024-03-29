import phonenumbers
from django import forms

from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta

from financial_server.core.fields import MobilePhoneField

from django.utils import timezone

from financial_server.apps.users.models import User, Profile
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm

from financial_server.core.utils import normalize_phone

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
    phone = MobilePhoneField()
    birthday = forms.CharField()
    password = forms.CharField()

    def clean_email(self) -> str:
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Pengguna dengan email ini sudah ada',
                                        code='duplicate_email')
        return email

    def clean_phone(self) -> str:
        try:
            phone = normalize_phone(self.cleaned_data['phone'])
        except phonenumbers.NumberParseException:
            raise forms.ValidationError('Nomor ponsel tidak valid.', code='invalid_mobile_number')

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

    def clean(self) -> dict:
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        return cleaned_data

    def save(self) -> User:
        user: User = User.objects.create(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            phone=normalize_phone(self.cleaned_data['phone']),
        )

        user.set_password(self.cleaned_data['password'])

        Profile.objects.create(
            user=user,
            birthday=self.cleaned_data['birthday'],
        )
        return user


class EditProfileForm(forms.Form):
    name = forms.CharField()
    phone = MobilePhoneField()
    birthday = forms.CharField()
    gender = forms.ChoiceField(choices=Profile.GENDER)
    address = forms.CharField(required=False)
    
    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_phone(self) -> str:
        try:
            phone = normalize_phone(self.cleaned_data['phone'])
        except phonenumbers.NumberParseException:
            raise forms.ValidationError('Nomor ponsel tidak valid.', code='invalid_mobile_number')

        if self.user.phone != phone and User.objects.filter(phone=phone).exists():
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

    def save(self, user: User) -> User:
        user.name = self.cleaned_data['name']
        user.phone = normalize_phone(self.cleaned_data['phone'])
        user.save(update_fields=['name', 'phone'])
        
        defaults = {
            'birthday': self.cleaned_data['birthday'],
            'gender': self.cleaned_data['gender']
        }
        
        if self.cleaned_data['address']:
            defaults['address'] = self.cleaned_data['address']

        Profile.objects.update_or_create(
            user=user,
            defaults=defaults
        )

        return user


class EditPhotoForm(forms.Form):
    photo = forms.ImageField(required=True)

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self) -> User:
        self.user.profile.photo = self.cleaned_data['photo']
        self.user.profile.save(update_fields=['photo'])

        return self.user
