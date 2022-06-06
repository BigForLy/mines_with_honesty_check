from abc import ABC, abstractmethod
from typing import Any
from authentication.models import User
from bomb_game.models import Bomb
from django.db import models

from services.game_state import Context, StateEndGame, StateWinGame, State


# class AbstractMoney(ABC):

#     @abstractmethod
#     def win(self, instance: models.Model) -> None:
#         pass

#     @abstractmethod
#     def lose(self, instance: models.Model) -> None:
#         pass

#     @abstractmethod
#     def end(self, user, instance: models.Model) -> None:
#         pass


# class MoneyBomb(AbstractMoney):

#     @staticmethod
#     def win(instance: Bomb) -> None:
#         return int(
#             1.2 * instance.price_difference + 0.2 * instance.start_sum
#         )

#     # @staticmethod
#     # def lose(instance: Bomb) -> None:
#     #     return -1 * instance.start_sum
#     #     # instance.price_difference = -1 * instance.start_sum

#     @staticmethod
#     def end(instance: Bomb) -> None:
#         # если есть пересечение открытых полей и бомб, игра проиграна
#         if len(set(instance.opened) & set(instance.bomb_in)):
#             return 0
#         return instance.price_difference + instance.start_sum


class MoneyManager:
    """
    strategy
    """

    # @classmethod
    # def create(cls, model: models.Model):
    #     if model == Bomb:
    #         strategy = MoneyBomb
    #     else:
    #         raise RuntimeError('Невозможно найти менеджер %s' % str(model))

    #     return cls(strategy)

    def __init__(self) -> None:
        # self.__strategy = strategy
        self.__state = None

    # def __call__(self, instance: models.Model) -> Any:
    #     self.__instance = instance

    # def win(self) -> int:
    #     return self.__strategy.win(self.__instance)

    # def end(self) -> int:
    #     return self.__strategy.end(self.__instance)

    # def user(self):
    #     return MoneyUser()
    #     # self.__instance.user.balance += self.__state.user()
    #     # self.__instance.user.save()

    # def game(self):
    #     pass
        # self.__instance.price_difference += self.__state.game()
        # self.__instance.save()
    def calculation(self):
        self.__state.calculation()  # проверка что state not none

    def state_change(self, instance, cls: State):
        self.__instance = instance
        self.__state = Context(cls(self.__instance))
