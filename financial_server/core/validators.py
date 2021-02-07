from id_phonenumbers import parse
from phonenumbers import phonenumberutil

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def validate_mobile_phone(phone_number):
    # Indonesia only accept mobile phone
    try:
        number = parse(phone_number)
    except phonenumberutil.NumberParseException:
        raise ValidationError('Please enter a valid mobile phone number.', code='invalid_mobile_number')

    if number.is_mobile:
        return True

    raise ValidationError('Please enter a valid mobile phone number.')


def validate_email_address(email):
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(f'{email} is not a valid email', code='invalid')

    if email.endswith('.'):
        raise ValidationError('Email cannot end with \'.\' (dot), please check again')
    else:
        return True
