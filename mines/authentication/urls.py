from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
)

urlpatterns = [
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('signin/', LoginAPIView.as_view(), name='signin'),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
]
