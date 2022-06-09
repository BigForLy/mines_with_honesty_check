from services.redis import RedisClient
from .models import Bomb
from mines.celery import app
from services.game_state import StateEndGame, Context


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
        state = Context()
        state.to_application(instance, StateEndGame())
        state.money_calculation()
        return True
    return False
