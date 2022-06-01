from django_redis import get_redis_connection
from datetime import timedelta


class RedisClient:

    def __init__(self, key, time_minute_delta) -> None:
        self._client = get_redis_connection("default")
        self.key = key
        self.time_minute_delta = time_minute_delta

    def get(self):
        result = self._client.get(self.key)
        if isinstance(result, bytes):
            result = result.decode("utf-8")
        return result

    def create_value(self, value):
        if not isinstance(value, str):
            value = str(value)
        self.__setex(value)

    def __setex(self, value):
        self._client.setex(self.key,
                           timedelta(minutes=self.time_minute_delta),
                           value=value
                           )
