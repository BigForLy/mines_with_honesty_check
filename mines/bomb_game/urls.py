from django.urls import path

from .views import (BombStartView, BombMoveView, BombEndView)


urlpatterns = [
    path('start/', BombStartView.as_view(), name='start_bomb_game'),
    path('move/', BombMoveView.as_view(), name='move_bomb_game'),
    path('end/', BombEndView.as_view(), name='end_bomb_game'),
]
