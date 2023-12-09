from shortuuid.django_fields import ShortUUIDField

from django.db import models

from common.models import TimestampedModel


class Token(TimestampedModel, models.Model):
    id = ShortUUIDField(length=20, prefix='token_', primary_key=True)  # noqa: A003
    name = models.CharField('name', max_length=200, default='')
    decimals = models.IntegerField('decimals', null=True)
    symbol = models.CharField('symbol', max_length=100, default='')
    is_complete = models.BooleanField('is complete', default=False)
    address = models.CharField('address', max_length=200, blank=False, unique=True)
    coingecko_id = models.CharField('coingecko identifier', max_length=200, default='')
