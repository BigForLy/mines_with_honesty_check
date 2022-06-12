from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
from authentication.models import User


class Bomb(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    start_sum = models.PositiveIntegerField()

    price_difference = models.PositiveIntegerField(
        default=0
    )

    opened = ArrayField(
        models.PositiveIntegerField(),
        default=list,
        blank=False
    )

    bomb_in = ArrayField(
        models.PositiveIntegerField(),
        default=list,
        blank=False
    )

    hash_bomb_in = models.JSONField()

    class Meta:
        db_table = 'bomb'
        verbose_name = 'Игра бомбочки'
