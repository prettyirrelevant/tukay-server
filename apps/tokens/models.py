from django.db import models

from common.models import TimestampedModel, UUIDModel


class Token(UUIDModel, TimestampedModel, models.Model):
    name = models.CharField('name', max_length=200, default='')
    decimals = models.IntegerField('decimals', null=True)
    symbol = models.CharField('symbol', max_length=100, default='')
    is_complete = models.BooleanField('is complete', default=False)
    address = models.CharField('address', max_length=200, blank=False, unique=True)
    coingecko_id = models.CharField('coingecko identifier', max_length=200, default='')
