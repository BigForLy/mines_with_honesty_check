from abc import ABC, abstractmethod

from ..models import Bomb
from django.db import models


class AbstractMoney(ABC):

    @abstractmethod
    def win(self, instance) -> None:
        pass

    @abstractmethod
    def lose(self, instance) -> None:
        pass

    @abstractmethod
    def end(self, user, instance) -> None:
        pass


class MoneyBomb(AbstractMoney):

    def win(self, instance: Bomb) -> None:
        instance.price_difference = int(
            1.2 * instance.price_difference + 0.2 * instance.start_sum
        )

    def lose(self, instance: Bomb) -> None:
        instance.price_difference = -1 * instance.start_sum

    def end(self, user, instance: Bomb) -> None:
        # если есть пересечение открытых полей и бомб, игра проиграна
        if len(set(instance.opened) & set(instance.bomb_in)):
            self.lose(instance)
            instance.save()
        user.balance += instance.price_difference
        user.save()


class MoneyManager:
    """
    strategy
    """

    @classmethod
    def create(cls, gamename: str):
        if gamename == 'bomb':
            strategy = MoneyBomb
        else:
            raise RuntimeError('Невозможно найти менеджер %s' % gamename)

        return cls(strategy)

    def __init__(self, strategy: AbstractMoney) -> None:
        self._strategy = strategy()

    def win(self, instance: models.Model):
        self._strategy.win(instance)

    def end(self, user, instance: models.Model):
        self._strategy.end(user, instance)
