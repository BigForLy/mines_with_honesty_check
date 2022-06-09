from abc import ABC, abstractmethod

from django.db import models
from django.conf import settings
from rest_framework import exceptions
from bomb_game.exceptions import Conflict
from authentication.models import User
from datetime import timedelta
from bomb_game.tasks import celery_end_game
from bomb_game.versions import AbstractVersion
from services.decode import AbstractDecode
# from services.decode import SHA256Decode
from services.game_state import StateLoseGame, StateStartGame, StateEndGame, StateWinGame, Context
from bomb_game.serializers import BombOutputSerializer
from bomb_game.models import Bomb
from .redis import RedisClient
import random


class AbstaractGame(ABC):

    def __init__(self, model, user, game_time, version_cls) -> None:
        self.model: models.Model = model
        self.user: User = user
        self.__redis_client = RedisClient(
            key=user.id,
            time_minute_delta=game_time
        )
        self.__game_token = self._game_token()
        self.__instance = None
        # self._money_manager = None
        self._state: Context = Context()
        self._version_cls: AbstractVersion = version_cls
        self._decoder: AbstractDecode = version_cls.decoder()

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
        return self.__redis_client.get()

    def __check_game_started(self):
        if not self.__game_token:
            raise exceptions.NotFound("Game not started.")

    def __check_not_game_started(self):
        if self.__game_token:
            raise Conflict()

    def _get_instance(self):
        self.__check_game_started()

        if not self.__instance:
            try:
                self.__instance = self.model.objects.get(id=self.__game_token)
            except self.model.DoesNotExist:
                raise exceptions.NotFound("Game not started.")

        return self.__instance

    def _create_game(self, *, start_sum, bomb_in):
        self.__check_not_game_started()

        self.__instance = self.model.objects.create(
            user=self.user,
            start_sum=start_sum,
            bomb_in=bomb_in,
            hash_bomb_in=self._decoder.decode(str(bomb_in))
        )
        self.__celery_create_worker()
        self.__redis_client.create_value(value=self.__instance.pk)

        return self.__instance

    def _redis_delete(self):
        self.__redis_client.delete_value()

    def __celery_create_worker(self):
        start_time = self.__instance.started_at + \
            timedelta(minutes=settings.BOMB_GAME_TIME_IN_MINUTES)
        celery_end_game.apply_async(
            (self.user.id, str(self.__instance.pk)),
            eta=start_time,
            retry=False,
            ignore_result=True
        )

    def _state_to_application(self, cls):
        self._state.to_application(self.__instance, cls())

    def _state_transition_to(self, cls):
        self._state.transition_to(cls())


class BombGame(AbstaractGame):

    def __init__(self, user, version_cls) -> None:
        super().__init__(
            model=Bomb,
            user=user,
            game_time=settings.BOMB_GAME_TIME_IN_MINUTES,
            version_cls=version_cls
        )

    def start(self, data):
        instance = self._create_game(
            start_sum=data['start_sum'],
            bomb_in=random.sample(
                settings.BOMB_GAME_COUNT_ELEMENT,
                data["bomb"]
            )
        )
        self._state_to_application(StateStartGame)
        self._state.money_calculation()

        return BombOutputSerializer(
            instance,
            context={
                "game_log": "Game started."
            }
        )

    def move(self, data):
        instance = self._get_instance()
        self._state_to_application(StateWinGame)

        move = data.get('move')
        if move in instance.opened:
            raise Conflict("Move has already been made. Make another move.")

        instance.opened.append(move)
        instance.save()

        if move in instance.bomb_in:
            self._state_transition_to(StateLoseGame)
            return self.end()

        self._state.money_calculation()

        return BombOutputSerializer(
            instance,
            context={
                "game_log": "Movement successful."
            }
        )

    def end(self):
        instance = self._get_instance()
        self._state_to_application(StateEndGame)

        self._redis_delete()

        self._state.money_calculation()

        return BombOutputSerializer(
            instance,
            context={
                "game_log": "Endgame successful.",
                "bomb_in": instance.bomb_in,
                "hash_bomb_text": str(instance.bomb_in)
            }
        )
