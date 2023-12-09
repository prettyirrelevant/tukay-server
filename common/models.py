from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField('created at', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('updated at', auto_now=True, db_index=True)

    class Meta:
        abstract = True
