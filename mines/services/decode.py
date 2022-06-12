from abc import ABC, abstractmethod
import hashlib
from base64 import b64encode
from Crypto.Cipher import AES


class AbstractEncrypt(ABC):

    @abstractmethod
    def encrypt(self, value: str):
        pass


class SHA256Encrypt(AbstractEncrypt):

    def encrypt(self, value: str) -> dict:
        return {"algorithm": "sha-256",
                "hash": hashlib.sha256(value.encode('utf-8')).hexdigest(),
                "secret": ""}


class AESEncrypt(object):

    def encrypt(self, value: str) -> dict:
        key = 'abcdefg123456789'
        key = key.encode()
        cypto_obj = AES.new(key, AES.MODE_ECB)
        encrypted_data = cypto_obj.encrypt(self.__pkcs5_pad(value))
        return {"algorithm": "AES",
                "hash": b64encode(encrypted_data).decode(),
                "secret": key.decode()}

    def __pkcs5_pad(self, s, BLOCK_SIZE=16):
        return (s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(
            BLOCK_SIZE - len(s) % BLOCK_SIZE
        )).encode('utf-8')
