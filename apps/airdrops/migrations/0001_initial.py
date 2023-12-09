# Generated by Django 5.0 on 2023-12-09 08:43

import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('tokens', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airdrop',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated at')),
                (
                    'id',
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet=None, length=20, max_length=28, prefix='airdrop_', primary_key=True, serialize=False
                    ),
                ),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('merkle_root', models.BinaryField(verbose_name='merkle_root')),
                ('amount', models.PositiveBigIntegerField(verbose_name='amount')),
                ('expected_claims', models.PositiveBigIntegerField(verbose_name='expected claims')),
                ('contract_index', models.BigIntegerField(unique=True, verbose_name='contract index')),
                ('tx_reference', models.CharField(max_length=66, unique=True, verbose_name='transaction reference')),
                (
                    'owner',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='created_airdrops',
                        to='accounts.account',
                        to_field='address',
                        verbose_name='owner',
                    ),
                ),
                (
                    'token',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='token_airdrops',
                        to='tokens.token',
                        to_field='address',
                        verbose_name='token',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated at')),
                (
                    'id',
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet=None, length=20, max_length=26, prefix='claim_', primary_key=True, serialize=False
                    ),
                ),
                ('amount', models.PositiveBigIntegerField(verbose_name='amount')),
                ('tx_reference', models.CharField(max_length=66, unique=True, verbose_name='transaction reference')),
                (
                    'account',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='claimed_airdrops',
                        to='accounts.account',
                        to_field='address',
                        verbose_name='owner',
                    ),
                ),
                (
                    'airdrop',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='claims',
                        to='airdrops.airdrop',
                        to_field='contract_index',
                        verbose_name='airdrop',
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name='claim',
            constraint=models.UniqueConstraint(fields=('account', 'airdrop'), name='account_airdrop_claim_unique'),
        ),
    ]
