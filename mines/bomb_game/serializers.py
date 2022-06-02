from rest_framework import serializers
from django.conf import settings
from .models import Bomb


class BombOutputSerializer(serializers.ModelSerializer):

    game_token = serializers.UUIDField(source='pk')
    bomb_in = serializers.SerializerMethodField()
    bomb_count = serializers.SerializerMethodField()
    game_duration = serializers.SerializerMethodField()
    game_log = serializers.SerializerMethodField()

    def get_bomb_in(self, obj):
        return self.context.get('bomb_in', [])

    def get_bomb_count(self, obj):
        return self.context.get('bomb_count')

    def get_game_duration(self, obj):
        return settings.BOMB_GAME_TIME_IN_MINUTES

    def get_game_log(self, obj):
        return self.context.get('game_log')

    class Meta:
        model = Bomb
        fields = ['game_token', 'opened', 'bomb_in', 'bomb_count', 'price_difference',
                  'start_sum', 'started_at', 'game_duration', 'game_log']


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
