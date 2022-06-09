from abc import ABC, abstractmethod

from services.decode import SHA256Decode


class AbstractVersion(ABC):
    
    @abstractmethod
    def decoder(self):
        pass


class V1Version(AbstractVersion):

    @staticmethod
    def decoder():
        return SHA256Decode


class VerisionStrategy:  # неправильный паттерн, прототип или наоборот стратегия

    @classmethod
    def create(cls, version):
        if version == 'v1':
            return V1Version
        elif version == 'v2':
            pass
        else:
            raise RuntimeError('Невозможно найти версию %s' %
                               version)  # todo: exception
