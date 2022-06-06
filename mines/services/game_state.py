from __future__ import annotations
from abc import ABC, abstractmethod


class Context:
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов. Он также
    хранит ссылку на экземпляр подкласса Состояния, который отображает текущее
    состояние Контекста.
    """

    _state = None
    """
    Ссылка на текущее состояние Контекста.
    """

    def __init__(self, state: State) -> None:
        self.transition_to(state)

    def transition_to(self, state: State):
        """
        Контекст позволяет изменять объект Состояния во время выполнения.
        """

        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    Контекст делегирует часть своего поведения текущему объекту Состояния.
    """

    # def user(self):
    #     return self._state.user()

    # def game(self):
    #     return self._state.game()
    def calculation(self):
        self._state.user()
        self._state.game()


class State(ABC):
    """
    Базовый класс Состояния объявляет методы, которые должны реализовать все
    Конкретные Состояния, а также предоставляет обратную ссылку на объект
    Контекст, связанный с Состоянием. Эта обратная ссылка может использоваться
    Состояниями для передачи Контекста другому Состоянию.
    """

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def user(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def game(self) -> None:
        raise NotImplementedError()


class StateStartGame(State):

    def __init__(self, game_instance) -> None:
        super().__init__()
        self.__game_instance = game_instance

    def user(self) -> None:
        self.__game_instance.user.balance += -1 * self.__game_instance.start_sum
        self.__game_instance.user.save()

    def game(self) -> None:
        pass


class StateWinGame(State):

    def __init__(self, game_instance) -> None:
        super().__init__()
        self.__game_instance = game_instance

    def user(self) -> None:
        pass

    def game(self) -> None:
        self.__game_instance.price_difference += int(
            1.2 * self.__game_instance.price_difference +
            0.2 * self.__game_instance.start_sum
        )
        self.__game_instance.save()


class StateLoseGame(State):

    def __init__(self, game_instance) -> None:
        super().__init__()
        self.__game_instance = game_instance

    def user(self) -> None:
        return 0

    def game(self) -> None:
        return -1 * self.__game_instance.start_sum


class StateEndGame(State):

    def __init__(self, game_instance) -> None:
        super().__init__()
        self.__game_instance = game_instance

    def user(self) -> None:
        return self.__game_instance.price_difference + self.__game_instance.start_sum

    def game(self) -> None:
        return None
