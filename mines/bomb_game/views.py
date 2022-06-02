from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services.games import BombGame
from .serializers import (BomdGameStartSerializer, BomdGameMoveSerializer)


class BombStartView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BomdGameStartSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context=request.user
        )
        serializer.is_valid(raise_exception=True)

        data = BombGame(user=request.user)\
            .start(serializer.data)\
            .data

        return Response(data, status=status.HTTP_201_CREATED)


class BombMoveiew(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BomdGameMoveSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context=request.user
        )
        serializer.is_valid(raise_exception=True)

        data = BombGame(user=request.user)\
            .move(serializer.data)\
            .data

        return Response(data, status=status.HTTP_200_OK)


class BombEndiew(APIView):

    def post(self, request):
        data = BombGame(user=request.user)\
            .end()\
            .data

        return Response(data, status=status.HTTP_200_OK)
