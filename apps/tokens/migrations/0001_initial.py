# Generated by Django 5.0 on 2023-12-05 18:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id'
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated at')),
                ('name', models.CharField(default='', max_length=200, verbose_name='name')),
                ('decimals', models.IntegerField(null=True, verbose_name='decimals')),
                ('symbol', models.CharField(default='', max_length=100, verbose_name='symbol')),
                ('is_complete', models.BooleanField(default=False, verbose_name='is complete')),
                ('address', models.CharField(max_length=200, unique=True, verbose_name='address')),
                ('coingecko_id', models.CharField(default='', max_length=200, verbose_name='coingecko identifier')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]