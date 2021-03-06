from rest_framework import serializers
from django.conf import settings
from .models import Bomb
import copy


class BombOutputSerializer(serializers.ModelSerializer):

    game_token = serializers.UUIDField(source='pk')
    bomb_in = serializers.SerializerMethodField()
    bomb_count = serializers.SerializerMethodField()
    game_duration = serializers.SerializerMethodField()
    game_log = serializers.SerializerMethodField()
    hash_bomb_in = serializers.SerializerMethodField()

    def get_bomb_in(self, obj) -> list[int]:
        return self.context.get('bomb_in', [])

    def get_bomb_count(self, obj) -> int:
        return len(obj.bomb_in)

    def get_game_duration(self, obj) -> int:
        return settings.BOMB_GAME_TIME_IN_MINUTES

    def get_game_log(self, obj) -> str:
        return self.context.get('game_log')

    def get_hash_bomb_in(self, obj) -> dict:
        data: dict = copy.deepcopy(obj.hash_bomb_in)
        # если приходит hash_bomb_text значит игра закончена, иначе удаляем упоминание secret
        if self.context.get('hash_bomb_text'):
            data.update({"text": self.context.get('hash_bomb_text')})
        else:
            data.pop('secret')
        return data

    class Meta:
        model = Bomb
        fields = ['game_token', 'opened', 'bomb_in', 'bomb_count', 'price_difference',
                  'start_sum', 'started_at', 'game_duration', 'hash_bomb_in', 'game_log']


class BomdGameStartSerializer(serializers.Serializer):

    bomb = serializers.IntegerField()

    start_sum = serializers.IntegerField()

    def validate(self, data):
        bomb = data.get('bomb')
        start_sum = data.get('start_sum')

        if bomb is None or  \
                not settings.MIN_COUNT_BOMB <= bomb <= settings.MAX_COUNT_BOMB or \
                not isinstance(bomb, int):
            raise serializers.ValidationError(
                'Bomb incorrect value.'
            )

        if start_sum is None or \
                not isinstance(start_sum, int):
            raise serializers.ValidationError(
                'Start sum incorrect value.'
            )

        if not 0 < start_sum < self.context.balance:
            raise serializers.ValidationError(
                'User balance encorrect.'
            )
        return super().validate(data)


class BomdGameMoveSerializer(serializers.Serializer):

    move = serializers.IntegerField()

    def validate(self, data):
        move = data.get('move')

        if not move or move not in settings.BOMB_GAME_COUNT_ELEMENT:
            raise serializers.ValidationError(
                'Move incorrect value.'
            )

        return super().validate(data)


class BombHistorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Bomb
        fields = ['username', 'price_difference']
