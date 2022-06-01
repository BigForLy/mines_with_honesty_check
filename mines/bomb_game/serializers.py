from rest_framework import serializers

from django.conf import settings


class BombOutputSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            "gameToken": instance.pk,
            "opened": instance.opened,
            "gameLog": self.context.get('gameLog'),
            "gameStartedAt": instance.started_at,
            "gameDuration": settings.BOMB_GAME_TIME_IN_MINUTES
        }


class BomdStartGameSerializer(serializers.Serializer):

    bomb = serializers.IntegerField()

    amount = serializers.IntegerField()

    def validate(self, data):
        bomb = data.get('bomb', None)
        amount = data.get('amount', None)

        if bomb is None or  \
                not settings.MIN_COUNT_BOMB <= bomb <= settings.MAX_COUNT_BOMB or \
                not isinstance(bomb, int):
            raise serializers.ValidationError(
                'Bomb incorrect value.'
            )

        if amount is None or \
                not isinstance(amount, int):
            raise serializers.ValidationError(
                'Amount incorrect value.'
            )

        if self.context.quantity < amount:
            raise serializers.ValidationError(
                'User quantity encorrect.'
            )
        return super().validate(data)
