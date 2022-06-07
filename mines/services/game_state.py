from __future__ import annotations
from abc import ABC, abstractmethod


class Context:

    _state = None

    def __init__(self) -> None:
        self._instance = None
        self._states = self.__get_states()

    def __get_states(self):
        return [StateStartGame, StateWinGame, StateEndGame, StateLoseGame]

    def to_application(self, instance, cls: State) -> bool:
        self._instance = instance
        return self.transition_to(cls)

    def transition_to(self, state: State) -> bool:
        if self.__machine_state(state):
            self._state.context = self
            return True
        return False

    def __machine_state(self, state):
        if self._state is None:
            self._state = state
            return True
        else:
            index = self._states.index(type(self._state))
            if self._states.index(type(state)) > index:
                self._state = self._state = state
                return True
            else:
                return False

    def money_calculation(self):
        self._state.user()
        self._state.game()


class State(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def user(self) -> None:
        pass

    @abstractmethod
    def game(self) -> None:
        pass


class StateStartGame(State):

    def user(self) -> None:
        instance = self.context._instance
        instance.user.balance += -1 * instance.start_sum
        instance.user.save()

    def game(self):
        pass


class StateWinGame(State):

    def user(user):
        pass

    def game(self) -> None:
        instance = self.context._instance
        instance.price_difference += int(
            1.2 * instance.price_difference +
            0.2 * instance.start_sum
        )
        instance.save()


class StateLoseGame(State):

    def user(self):
        pass

    def game(self) -> None:
        instance = self.context._instance
        instance.price_difference = -1 * instance.start_sum
        instance.save()


class StateEndGame(State):

    def user(self) -> None:
        instance = self.context._instance
        instance.user.balance += instance.price_difference + instance.start_sum
        instance.user.save()

    def game(self):
        pass
