from django.urls import reverse
from rest_framework.test import APITestCase
from django_redis import get_redis_connection
from django.conf import settings


class TestStartGameSetUp(APITestCase):

    def setUp(self) -> None:
        self.start_bomb_game_url = reverse('start_bomb_game')
        self.move_bomb_game_url = reverse('move_bomb_game')
        self.end_bomb_game_url = reverse('end_bomb_game')

        self.bomb_game_start_data = {
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


class TestSetUpAlreadyCreatedModel(TestStartGameSetUp):

    def setUp(self) -> None:
        super().setUp()
        self.created_game = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_start_data
        )


class TestMoveGameSetUp(TestSetUpAlreadyCreatedModel):

    def setUp(self) -> None:
        self.bomb_game_move_data = {
            "move": 3
        }
        range_element = settings.BOMB_GAME_COUNT_ELEMENT
        # ограничиваем область, чтобы точно быть уверенными где бомбы
        settings.BOMB_GAME_COUNT_ELEMENT = range(0, 3)
        super().setUp()
        # восстанавливаем изначальную последовательность
        settings.BOMB_GAME_COUNT_ELEMENT = range_element


class TestMoney(TestStartGameSetUp):

    def setUp(self) -> None:
        self.user_url = reverse('user')
        return super().setUp()
