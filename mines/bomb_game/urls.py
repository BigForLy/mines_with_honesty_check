from django.urls import path

from .views import BombView


urlpatterns = [
    path('', BombView.as_view())
]
