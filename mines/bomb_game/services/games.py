from abc import abstractmethod
from ..serializers import HighScoreSerializer
from ..models import Bomb
from django.db import models
import random
from rest_framework import exceptions
from .redis import RedisClient


class AbstaractGame:

    def __init__(self, model, user) -> None:
        self.model: models.Model = model
        self.user = user
        self.redis_client = RedisClient(
            key=user.id,
            time_minute_delta=5
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
        super().__init__(Bomb, user)

    def start(self, data):
        if self.token:
            raise exceptions.NotFound()  # enother code

        instanse = self.model.objects.create(
            user=self.user,
            start_sum=data['amount'],
            bomb_in=random.sample(range(25), data["bomb"])
        )
        self.redis_client.create_value(value=instanse.pk)
        serializer = HighScoreSerializer(
            instanse, context={"gameLog": "Game started."})
        data = serializer.data

        return data

    def move(self):
        if not self.token:
            raise exceptions.NotFound()
