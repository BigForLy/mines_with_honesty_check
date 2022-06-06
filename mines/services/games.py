from abc import abstractmethod

from django.db import models
from django.conf import settings
from rest_framework import exceptions
from bomb_game.exceptions import Conflict
from authentication.models import User
from datetime import timedelta
from bomb_game.tasks import celery_end_game
from services.game_state import Context, State, StateLoseGame, StateStartGame, StateEndGame, StateWinGame
from services.money import MoneyManager
from bomb_game.serializers import BombOutputSerializer
from bomb_game.models import Bomb
from .redis import RedisClient
import random


class AbstaractGame:

    def __init__(self, model, user, game_time) -> None:
        self.model: models.Model = model
        self.user: User = user
        self.__redis_client = RedisClient(
            key=user.id,
            time_minute_delta=game_time
        )
        self.__game_token = self._game_token()
        self.__instance = None
        self._money_manager = MoneyManager()
        self.__state = None

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
            bomb_in=bomb_in
        )
        self.__celery_create_worker()
        self.__redis_client.create_value(value=self.__instance.pk)
        # self._money_manager.state_change(self.__instance, StateStartGame)

        # self._money_manager.calculation()
        return self.__instance

    def _state_change(self, cls: State):
        self.__state = Context(cls(self.__instance))

    def _end_game(self):
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


class BombGame(AbstaractGame):

    def __init__(self, user) -> None:
        super().__init__(
            model=Bomb,
            user=user,
            game_time=settings.BOMB_GAME_TIME_IN_MINUTES
        )

    def start(self, data):
        instance = self._create_game(
            start_sum=data['start_sum'],
            bomb_in=random.sample(
                settings.BOMB_GAME_COUNT_ELEMENT,
                data["bomb"]
            )
        )
        self.__state = StateStartGame

        return BombOutputSerializer(
            instance,
            context={
                "game_log": "Game started."
            }
        )

    def move(self, data):
        instance = self._get_instance()
        self.__state = StateWinGame
        # self._money_manager.state_change(instance, StateWinGame)

        move = data.get('move')
        if move in instance.opened:
            raise Conflict("Move has already been made. Make another move.")

        instance.opened.append(move)

        if move in instance.bomb_in:
            self.__state = StateLoseGame
            return self.end()

        # self._money_manager.calculation()

        instance.save()

        return BombOutputSerializer(
            instance,
            context={
                "game_log": "Movement successful."
            }
        )

    def end(self):
        instance = self._get_instance()
        self.__state = StateEndGame
        # self._money_manager.state_change(instance, StateLoseGame)

        # money_end = self._money_manager.end()
        # self._money_manager.game()
        # self._money_manager.user()
        # self.manager.user.end()

        self._end_game()

        return BombOutputSerializer(
            instance,
            context={
                "game_log": "Endgame successful.",
                "bomb_in": instance.bomb_in
            }
        )
