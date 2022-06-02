from django.urls import path

from .views import (BombStartView, BombMoveiew, BombEndiew)


urlpatterns = [
    path('start/', BombStartView.as_view(), name='start_bomb_game'),
    path('move/', BombMoveiew.as_view(), name='move_bomb_game'),
    path('end/', BombEndiew.as_view(), name='end_bomb_game'),
]
