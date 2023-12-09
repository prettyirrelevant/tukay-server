# Generated by Django 5.0 on 2023-12-09 08:43

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated at')),
                (
                    'id',
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet=None, length=20, max_length=24, prefix='acc_', primary_key=True, serialize=False
                    ),
                ),
                ('address', models.CharField(max_length=42, unique=True, verbose_name='address')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
