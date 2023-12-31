from shortuuid.django_fields import ShortUUIDField

from django.db import models

from common.models import TimestampedModel


class Airdrop(TimestampedModel, models.Model):
    id = ShortUUIDField(length=20, prefix='airdrop_', primary_key=True)  # noqa: A003
    name = models.CharField('name', max_length=50, blank=False)
    merkle_root = models.BinaryField('merkle_root', blank=False)
    amount = models.PositiveBigIntegerField('amount', blank=False)
    merkle_leaves = models.JSONField('merkle_leaves', default=dict)
    expected_claims = models.PositiveBigIntegerField('expected claims', blank=False)
    contract_index = models.BigIntegerField('contract index', blank=False, unique=True)
    tx_reference = models.CharField('transaction reference', max_length=66, blank=False, unique=True)
    token = models.ForeignKey(
        'tokens.Token',
        verbose_name='token',
        to_field='address',
        related_name='token_airdrops',
        blank=False,
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        'accounts.Account',
        verbose_name='owner',
        to_field='address',
        related_name='created_airdrops',
        blank=False,
        on_delete=models.CASCADE,
    )


class Claim(TimestampedModel, models.Model):
    id = ShortUUIDField(length=20, prefix='claim_', primary_key=True)  # noqa: A003
    account = models.ForeignKey(
        'accounts.Account',
        verbose_name='account',
        to_field='address',
        related_name='claimed_airdrops',
        blank=False,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveBigIntegerField('amount', blank=False)
    tx_reference = models.CharField('transaction reference', max_length=66, blank=False, unique=True)
    airdrop = models.ForeignKey(
        'airdrops.Airdrop',
        verbose_name='airdrop',
        to_field='contract_index',
        related_name='claims',
        blank=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=('account', 'airdrop'), name='account_airdrop_claim_unique')]
