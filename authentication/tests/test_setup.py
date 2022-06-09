from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):

    def setUp(self) -> None:
        self.signin_url = reverse('signin')
        self.signup_url = reverse('signup')
        self.user_url = reverse('user')

        self.user_data = {
            "email": "template_email@pgadmin.org",
            "username": "template_username",
            "password": "template_password"
        }

        return super().setUp()
