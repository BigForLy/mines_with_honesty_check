from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .versions import VerisionStrategy
from services.games import BombGame
from .serializers import (BomdGameStartSerializer, BomdGameMoveSerializer)


class BombStartView(APIView):
    serializer_class = BomdGameStartSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context=request.user
        )
        serializer.is_valid(raise_exception=True)

        data = BombGame(user=request.user,
                        version_cls=VerisionStrategy.create(request.version))\
            .start(serializer.data)\
            .data

        return Response(data, status=status.HTTP_201_CREATED)


class BombMoveView(APIView):
    serializer_class = BomdGameMoveSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context=request.user
        )
        serializer.is_valid(raise_exception=True)

        data = BombGame(user=request.user,
                        version_cls=VerisionStrategy.create(request.version))\
            .move(serializer.data)\
            .data

        return Response(data, status=status.HTTP_200_OK)


class BombEndView(APIView):

    def post(self, request):
        data = BombGame(user=request.user,
                        version_cls=VerisionStrategy.create(request.version))\
            .end()\
            .data

        return Response(data, status=status.HTTP_200_OK)
