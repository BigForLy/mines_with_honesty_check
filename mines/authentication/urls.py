from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
)

urlpatterns = [
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('signin/', LoginAPIView.as_view(), name='signin'),
    path('', UserRetrieveUpdateAPIView.as_view(), name='user'),
]
