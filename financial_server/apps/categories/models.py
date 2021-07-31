from django.db import models

from financial_server.core.utils import FilenameGenerator

from thumbnails.fields import ImageField


class Category(models.Model):
    name = models.CharField(blank=True, null=True, max_length=64)
    logo = ImageField(upload_to=FilenameGenerator(prefix='category_logos'),
                      blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
