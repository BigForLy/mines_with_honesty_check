from abc import ABC, abstractmethod

from services.decode import (SHA256Decoder, AESCipher, AbstractDecode)


class AbstractVersion(ABC):

    @abstractmethod
    def decoder(self) -> AbstractDecode:
        pass


class V1Version(AbstractVersion):

    @property
    def decoder(self) -> AbstractDecode:
        return SHA256Decoder()


class V2Version(AbstractVersion):

    @property
    def decoder(self) -> AbstractDecode:
        return AESCipher()


class VerisionStrategy:

    @classmethod
    def create(cls, version):
        if version == 'v1':
            version_cls = V1Version
        elif version == 'v2':
            version_cls = V2Version
        else:
            raise RuntimeError('Невозможно найти версию %s' %
                               version)  # todo: exception

        return cls(version_cls)

    def __init__(self, version_cls: AbstractVersion) -> None:
        self.__version: AbstractVersion = version_cls()

    def encrypt(self, data) -> dict:
        return self.__version.decoder.encrypt(str(data))
