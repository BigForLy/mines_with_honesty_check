from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework import status

from bomb_game.models import Bomb
from .versions import VerisionStrategy
from services.games import BombGame
from .serializers import (BomdGameStartSerializer,
                          BomdGameMoveSerializer, BombOutputSerializer, BombHistorySerializer)
from drf_yasg.utils import swagger_auto_schema


class BombStartView(GenericAPIView):
    serializer_class = BomdGameStartSerializer

    @swagger_auto_schema(responses={201: BombOutputSerializer()})
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context=request.user
        )
        serializer.is_valid(raise_exception=True)

        data = BombGame(user=request.user,
                        strategy=VerisionStrategy.create(request.version))\
            .start(serializer.data)\
            .data

        return Response(data, status=status.HTTP_201_CREATED)


class BombMoveView(GenericAPIView):
    serializer_class = BomdGameMoveSerializer

    @swagger_auto_schema(responses={200: BombOutputSerializer()})
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context=request.user
        )
        serializer.is_valid(raise_exception=True)

        data = BombGame(user=request.user,
                        strategy=VerisionStrategy.create(request.version))\
            .move(serializer.data)\
            .data

        return Response(data, status=status.HTTP_200_OK)


class BombEndView(APIView):

    @swagger_auto_schema(responses={200: BombOutputSerializer()})
    def post(self, request):
        data = BombGame(user=request.user)\
            .end()\
            .data

        return Response(data, status=status.HTTP_200_OK)


class BombHistoryView(ListAPIView):

    serializer_class = BombHistorySerializer
    queryset = Bomb.objects.select_related('user').all()
