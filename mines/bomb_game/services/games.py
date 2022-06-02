from abc import abstractmethod

from django.db import models
from django.conf import settings
from rest_framework import exceptions
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
        # self.money_manager =
        self.game_token = self._game_token()

    @abstractmethod
    def start(self, data):
        pass

    @abstractmethod
    def move(self, data):
        pass

    @abstractmethod
    def end(self, instanse=None):
        pass

    def _game_token(self) -> bool:
        return self.redis_client.get()

    def _check_game_started(self):
        if not self.game_token:
            raise exceptions.NotFound("Game not started.")

    def _check_not_game_started(self):
        if self.game_token:
            raise Conflict()

    def _get_instanse(self):
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

        instanse = self.model.objects.create(
            user=self.user,
            start_sum=data['start_sum'],
            bomb_in=random.sample(
                settings.BOMB_GAME_COUNT_ELEMENT,
                data["bomb"]
            )
        )
        self.redis_client.create_value(value=instanse.pk)
        return BombOutputSerializer(
            instanse,
            context={
                "game_log": "Game started.",
                "bomb_count": len(instanse.bomb_in)
            }
        )

    def move(self, data):
        self._check_game_started()

        instanse = self._get_instanse()

        move = data.get('move')
        if move in instanse.opened:
            raise Conflict("Move has already been made. Make another move.")

        instanse.opened.append(move)

        if move in instanse.bomb_in:
            self.end(instanse)

        instanse.price_difference = int(
            1.2 * (instanse.price_difference + instanse.start_sum)
        )
        instanse.save()

        return BombOutputSerializer(
            instanse,
            context={
                "game_log": "Movement successful.",
                "bomb_count": len(instanse.bomb_in)
            }
        )

    def end(self, instanse=None):
        if not instanse:
            self._check_game_started()
            instanse = self._get_instanse()

        # если есть пересечение открытых полей и бомб, игра проиграна
        if len(set(instanse.opened) & set(instanse.bomb_in)):
            instanse.price_difference = -1 * instanse.start_sum
            instanse.save()

        self.redis_client.delete_value()

        return BombOutputSerializer(
            instanse,
            context={
                "game_log": "Endgame successful.",
                "bomb_in": instanse.bomb_in,
                "bomb_count": len(instanse.bomb_in)
            }
        )
