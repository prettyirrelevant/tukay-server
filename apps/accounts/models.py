from django.db import models

from common.models import UUIDModel, TimestampedModel


class Account(UUIDModel, TimestampedModel, models.Model):
    address = models.CharField('address', max_length=42, unique=True, blank=False)
