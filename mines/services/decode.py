from abc import ABC, abstractmethod
import hashlib


class AbstractDecode(ABC):

    @abstractmethod
    def decode(self):
        pass


class SHA256Decode(AbstractDecode):

    @staticmethod
    def decode(value: str) -> str:
        return hashlib \
            .sha256(value.encode('utf-8')) \
            .hexdigest()
