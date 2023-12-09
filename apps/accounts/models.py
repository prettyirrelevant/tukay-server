from shortuuid.django_fields import ShortUUIDField

from django.db import models

from common.models import TimestampedModel


class Account(TimestampedModel, models.Model):
    id = ShortUUIDField(length=20, prefix='acc_', primary_key=True)  # noqa: A003
    address = models.CharField('address', max_length=42, unique=True, blank=False)
