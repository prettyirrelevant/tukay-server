from shortuuid.django_fields import ShortUUIDField

from django.db import models

from common.models import TimestampedModel


class GiveawayType(models.TextChoices):
    TRIVIA = 'trivia'
    REGULAR = 'regular'
    ACTIVITY = 'activity'


class Giveaway(models.Model):
    id = ShortUUIDField(length=20, prefix='giv_', primary_key=True)  # noqa: A003
    name = models.CharField(max_length=45, blank=False)
    token = models.ForeignKey(
        'tokens.Token',
        verbose_name='token',
        to_field='address',
        related_name='token_giveaways',
        blank=False,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveBigIntegerField('amount', blank=False)
    owner = models.ForeignKey(
        'accounts.Account',
        verbose_name='owner',
        to_field='address',
        related_name='created_giveaways',
        blank=False,
        on_delete=models.CASCADE,
    )
    metadata = models.JSONField('metadata', default=dict)
    end_at = models.DateTimeField('end at', blank=False, null=False)
    start_at = models.DateTimeField('start at', blank=False, null=False)
    max_winners = models.PositiveSmallIntegerField('maximum winners', blank=False)
    max_participants = models.PositiveBigIntegerField('maximum participants', blank=False)
    giveaway_type = models.CharField('giveaway type', max_length=8, choices=GiveawayType.choices, blank=False)


class GiveawayWinner(TimestampedModel, models.Model):
    id = ShortUUIDField(length=20, prefix='giv_winner', primary_key=True)  # noqa: A003
    account = models.ForeignKey(
        'accounts.Account',
        verbose_name='account',
        to_field='address',
        related_name='created_giveaways',
        blank=False,
        on_delete=models.CASCADE,
    )
    giveaway = models.ForeignKey(
        'giveaways.Giveaway',
        verbose_name='giveaway',
        to_field='address',
        related_name='giveaway_winners',
        blank=False,
        on_delete=models.CASCADE,
    )


class GiveawayParticipant(TimestampedModel, models.Model):
    id = ShortUUIDField(length=20, prefix='giv_winner', primary_key=True)  # noqa: A003
    account = models.ForeignKey(
        'accounts.Account',
        verbose_name='account',
        to_field='address',
        blank=False,
        on_delete=models.CASCADE,
    )
    giveaway = models.ForeignKey(
        'giveaways.Giveaway',
        verbose_name='giveaway',
        to_field='address',
        related_name='giveaway_participants',
        blank=False,
        on_delete=models.CASCADE,
    )
    is_paid = models.BooleanField('is paid', default=False)
    is_winner = models.BooleanField('is winner', default=False)


class TriviaQA(TimestampedModel, models.Model):
    id = ShortUUIDField(length=20, prefix='trivia_qa_', primary_key=True)  # noqa: A003
    account = models.ForeignKey(
        'accounts.Account',
        verbose_name='account',
        to_field='address',
        blank=False,
        on_delete=models.CASCADE,
    )
    giveaway = models.ForeignKey(
        'giveaways.Giveaway',
        verbose_name='giveaway',
        to_field='address',
        blank=False,
        on_delete=models.CASCADE,
    )
    answers = models.JSONField('answers', default=dict)
    questions = models.JSONField('questions', default=dict)
    is_answered = models.BooleanField('is answered', default=False)
