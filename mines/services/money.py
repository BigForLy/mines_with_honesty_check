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


# class MoneyManager:

#     # @classmethod
#     # def create(cls, model: models.Model):
#     #     if model == Bomb:
#     #         strategy = MoneyBomb
#     #     else:
#     #         raise RuntimeError('Невозможно найти менеджер %s' % str(model))

#     #     return cls(strategy)

#     def __init__(self, state: State):
#         self.__state = Context(state)

#     def calculation(self):
#         self.__state.money_calculation()  # проверка что state not none
