from django.urls import reverse
from rest_framework.test import APITestCase
from django_redis import get_redis_connection


class TestSetUp(APITestCase):

    def setUp(self) -> None:
        self.start_bomb_game_url = reverse('start_bomb_game')

        self.bomb_game_data = {
            "bomb": 3,
            "start_sum": 10
        }

        response = self.client.post(
            reverse('signup'),
            {
                "email": "template_email@pgadmin.org",
                "username": "template_username",
                "password": "template_password"
            }
        )
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return super().setUp()

    def _clear_redis_keys(self):
        redis_client = get_redis_connection()
        keys = redis_client.keys('*')
        for key in keys:
            redis_client.delete(key)

    def tearDown(self) -> None:
        self._clear_redis_keys()
        return super().tearDown()


class TestSetUpAlreadyCreatedModel(TestSetUp):

    def setUp(self) -> None:
        super().setUp()
        self. created_game = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
