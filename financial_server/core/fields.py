from django import forms

import phonenumbers

from .utils import normalize_phone
from .validators import validate_mobile_phone


class MobilePhoneField(forms.Field):

    def clean(self, value):
        super(MobilePhoneField, self).clean(value)
        if value:
            validate_mobile_phone(value)
            try:
                value = normalize_phone(value)
            except phonenumbers.NumberParseException:
                raise forms.ValidationError('Mohon masukkan nomor ponsel yang benar')
        return value
