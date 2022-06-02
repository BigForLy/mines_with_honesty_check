from abc import abstractmethod

from django.db import models
from django.conf import settings
from rest_framework import exceptions

from ..services.money import MoneyManager
from ..exceptions import Conflict
from ..serializers import BombOutputSerializer
from ..models import Bomb
from .redis import RedisClient
import random


class AbstaractGame:

    def __init__(self, model, user, game_time) -> None:
        self.model: models.Model = model
        self.user = user
        self.redis_client = RedisClient(
            key=user.id,
            time_minute_delta=game_time
        )
        self.game_token = self._game_token()

    @abstractmethod
    def start(self, data):
        pass

    @abstractmethod
    def move(self, data):
        pass

    @abstractmethod
    def end(self, instance=None):
        pass

    def _game_token(self) -> bool:
        return self.redis_client.get()

    def _check_game_started(self):
        if not self.game_token:
            raise exceptions.NotFound("Game not started.")

    def _check_not_game_started(self):
        if self.game_token:
            raise Conflict()

    def _get_instance(self):
        try:
            return self.model.objects.get(id=self.game_token)
        except self.model.DoesNotExist:
            raise exceptions.NotFound("Game not started.")


class BombGame(AbstaractGame):

    def __init__(self, user) -> None:
        super().__init__(
            model=Bomb,
            user=user,
            game_time=settings.BOMB_GAME_TIME_IN_MINUTES
        )

    def start(self, data):
        self._check_not_game_started()

        instance = self.model.objects.create(
            user=self.user,
            start_sum=data['start_sum'],
            bomb_in=random.sample(
                settings.BOMB_GAME_COUNT_ELEMENT,
                data["bomb"]
            )
        )
        self.redis_client.create_value(value=instance.pk)
        return BombOutputSerializer(
            instance,
            context={
                "game_log": "Game started.",
                "bomb_count": len(instance.bomb_in)
            }
        )

    def move(self, data):
        self._check_game_started()

        instance = self._get_instance()

        move = data.get('move')
        if move in instance.opened:
            raise Conflict("Move has already been made. Make another move.")

        instance.opened.append(move)

        if move in instance.bomb_in:
            return self.end(instance)

        manager = MoneyManager.create('bomb')
        manager.win(instance)

        instance.save()

        return BombOutputSerializer(
            instance,
            context={
                "game_log": "Movement successful.",
                "bomb_count": len(instance.bomb_in)
            }
        )

    def end(self, instance=None):
        if not instance:
            self._check_game_started()
            instance = self._get_instance()

        manager = MoneyManager.create('bomb')
        manager.end(self.user, instance)

        self.redis_client.delete_value()

        return BombOutputSerializer(
            instance,
            context={
                "game_log": "Endgame successful.",
                "bomb_in": instance.bomb_in,
                "bomb_count": len(instance.bomb_in)
            }
        )
