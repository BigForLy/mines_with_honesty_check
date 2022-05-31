from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services.games import BombGame
from .serializers import BomdStartGameSerializer


class BombView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BomdStartGameSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context=request.user
        )
        serializer.is_valid(raise_exception=True)

        data = BombGame(user=request.user)\
            .start(request.data)

        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request):
        data = BombGame(user=request.user)\
            .move(request.data)

        return Response(data, status=status.HTTP_200_OK)
