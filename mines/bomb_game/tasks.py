from services.redis import RedisClient
from .models import Bomb
from mines.celery import app


@app.task
def add(x, y):
    return x / y


@app.task
def celery_end_game(key: str, game_instance_pk: str) -> bool:
    redis_client = RedisClient(key)
    value_from_key = redis_client.get()
    if value_from_key == game_instance_pk:
        redis_client.delete_value()
        try:
            instance = Bomb.objects.get(pk=game_instance_pk)
        except Bomb.DoesNotExist:
            raise

        instance.user.balance += instance.price_difference
        instance.user.save()
        return True
    return False
