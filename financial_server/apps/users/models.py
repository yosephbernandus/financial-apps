import datetime

from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)

from model_utils import Choices

from django.db import models
from django.contrib.sessions.backends.db import SessionStore

from financial_server.apps.permissions.constants import PermissionType
from financial_server.constants import PROVINCES
from financial_server.core.validators import validate_mobile_phone

from typing import Union, Any, Optional

from thumbnails.fields import ImageField


class CustomUserManager(UserManager):

    def create_user(self, name: str, email: str, phone: str, password: str, birthday: str,  # type: ignore
                    address: str = '', gender: int = 1, nik: str = '', **extra_fields: Any) -> 'User':  # type: ignore

        if not email and not phone:
            raise ValueError("Email or mobile phone is required")

        if email:
            email = email.lower()

        user = self.model(name=name, email=email, phone=phone)
        if password:
            user.set_password(password)
        user.save(using=self._db)  # type: ignore
        birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d").date()
        Profile.objects.create(user=user, address='',
                               birthday=birthday_date, gender=gender)

        return user

    def create_superuser(self, email: str, password: str, birthday: str = None, name: str = '', phone: str = '',  # type: ignore
                         **extra_fields: Any) -> 'User':  # type: ignore
        if birthday is None:
            birthday = '1970-01-01'

        user = self.create_user(name=name, email=email, phone=phone,
                                password=password, birthday=birthday, **extra_fields)
        user.is_staff = True
        user.is_active = True  # type: ignore
        user.is_superuser = True
        user.save(using=self._db)  # type: ignore
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField('email address', unique=True, max_length=254)
    nik = models.CharField(max_length=255, blank=True, null=True)

    province = models.PositiveSmallIntegerField(choices=PROVINCES, blank=True, null=True)

    is_staff = models.BooleanField(
        'Can access backoffice',
        default=False,
        help_text='Whether the user can log into backoffice.'
    )

    date_joined = models.DateTimeField(default=timezone.localtime)
    has_incorrect_email = models.BooleanField(default=False)
    phone = models.CharField(verbose_name='Mobile Number', max_length=30,
                             db_index=True, validators=[validate_mobile_phone])
    is_verified = models.BooleanField(default=False)
    backoffice_permissions = models.ManyToManyField('permissions.Permission', blank=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        return self.name

    def has_permission(self, permission: PermissionType) -> bool:
        # Cache hit
        if hasattr(self, '_cached_permissions'):
            return permission.value in self._cached_permissions  # type: ignore

        # Cache miss, query
        self._cached_permissions = set(
            self.backoffice_permissions.only('name')
                .values_list('name', flat=True)
        )
        return permission.value in self._cached_permissions

    @classmethod
    def from_session_key(cls, session_key: str, select_related: str) -> Optional['User']:
        session = SessionStore(session_key=session_key)

        if '_auth_user_id' not in session.keys():
            return None

        user_id = session['_auth_user_id']

        # In case user get deleted
        return cls.objects.select_related(select_related).filter(id=user_id).first()


class Profile(models.Model):
    from financial_server.core.utils import FilenameGenerator
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    place_of_birth = models.CharField(max_length=50, blank=True, null=True)
    photo = ImageField(upload_to=FilenameGenerator(prefix='profiles'),
                       blank=True, null=True)
    id_card_photo = ImageField(upload_to=FilenameGenerator(prefix='id_cards'),
                               blank=True, null=True)
    id_card_address = models.TextField(blank=True, default='')
    address = models.TextField(default='')
    postal_code = models.TextField(max_length=5, blank=True, default='')
    birthday = models.DateField()

    GENDER = Choices(
        (1, 'male', 'Laki-Laki'),
        (2, 'female', 'Perempuan'),
    )
    gender = models.PositiveSmallIntegerField(choices=GENDER, blank=True, null=True)

    RELIGION = Choices(
        (1, 'islam', 'Islam'),
        (2, 'katolik', 'Katolik'),
        (3, 'protestan', 'Protestan'),
        (4, 'hindu', 'Hindu'),
        (5, 'budha', 'Budha'),
        (6, 'konghucu', 'Konghucu'),
        (7, 'lain_lain', 'Lain-lain'),
    )
    religion = models.PositiveSmallIntegerField(choices=RELIGION, blank=True, null=True)
    notes = models.TextField(blank=True, default='')

    def __str__(self) -> str:
        return self.user.name or self.user.email

    def get_age(self, on_date: datetime.datetime = None) -> Union[None, int]:
        if not self.birthday:
            return None

        if on_date is None:
            on_date = timezone.localtime()

        is_on_date_smaller = (on_date.month, on_date.day) < (self.birthday.month, self.birthday.day)
        return on_date.year - self.birthday.year - is_on_date_smaller
