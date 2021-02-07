import os

from django.db import models
from django.template.defaultfilters import slugify

from django.utils import timezone


class FilenameGenerator(object):
    """
    Utility class to handle generation of file upload path
    """
    def __init__(self, prefix: str):
        self.prefix = prefix

    def __call__(self, instance: models.Model, filename: str) -> str:
        today = timezone.localdate()

        filepath = os.path.basename(filename)
        filename, extension = os.path.splitext(filepath)
        filename = slugify(filename)

        path = "/".join([
            self.prefix,
            str(today.year),
            str(today.month),
            str(today.day),
            filename + extension
        ])
        return path


try:
    from django.utils.deconstruct import deconstructible
    FilenameGenerator = deconstructible(FilenameGenerator)  # type: ignore
except ImportError:
    pass


def normalize_phone(number: str) -> str:
    if number.startswith('0'):
        number = number[1:]
    elif number.startswith('62'):
        number = '+' + number
    parse_phone_number = phonenumbers.parse(number, 'ID')
    phone_number = phonenumbers.format_number(
        parse_phone_number, phonenumbers.PhoneNumberFormat.E164)
    return phone_number
