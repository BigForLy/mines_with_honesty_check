from abc import abstractmethod
from ..serializers import BombOutputSerializer
from ..models import Bomb
from django.db import models
import random
from rest_framework import exceptions
from .redis import RedisClient
from django.conf import settings


class AbstaractGame:

    def __init__(self, model, user, game_time) -> None:
        self.model: models.Model = model
        self.user = user
        self.redis_client = RedisClient(
            key=user.id,
            time_minute_delta=game_time
        )
        self.token = self._game_token()

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def end(self):
        pass

    def _game_token(self) -> bool:
        return self.redis_client.get()


class BombGame(AbstaractGame):

    def __init__(self, user) -> None:
        super().__init__(Bomb, user, settings.BOMB_GAME_TIME_MINUTE)

    def start(self, data):
        if self.token:
            raise exceptions.NotFound("Game already exists.")  # enother code

        instanse = self.model.objects.create(
            user=self.user,
            start_sum=data['amount'],
            bomb_in=random.sample(
                range(settings.MIN_COUNT_BOMB-1, settings.MAX_COUNT_BOMB+1),
                data["bomb"]
            )
        )
        self.redis_client.create_value(value=instanse.pk)
        serializer = BombOutputSerializer(
            instanse,
            context={"gameLog": "Game started."}
        )

        return serializer.data

    def move(self, data):
        if not self.token:
            raise exceptions.NotFound("Game not started.")

        move = data.get('move')

        if not move:  # todo: create exceptions
            raise exceptions.NotFound("Not move.")

        instanse = self.model.objects.get(id=self.token)

        if move in instanse.opened:
            pass
            # raise exceptions.NotFound("Move in instanse.opened.") # todo: create exceptions

        if move in instanse.bomb_in:
            pass
            # raise exceptions.NotFound("Move in instanse.bomb_in.")  # todo: create end game

        instanse.opened.append(move)
        instanse.save()
        serializer = BombOutputSerializer(
            instanse,
            context={"gameLog": "Movement successful."}
        )

        return serializer.data
