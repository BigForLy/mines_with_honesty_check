from rest_framework import serializers
from django.conf import settings


class BombOutputSerializer(serializers.BaseSerializer):
    def to_representation(self, instance) -> dict:
        return {
            "game_token": instance.pk,
            "opened": instance.opened,
            "price_difference": instance.price_difference,
            "bomb_in": self.context.get('bomb_in', []),
            "game_log": self.context.get('game_log'),
            "game_started_at": instance.started_at,
            "game_duration": settings.BOMB_GAME_TIME_IN_MINUTES
        }


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

        if self.context.balance < start_sum:
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
