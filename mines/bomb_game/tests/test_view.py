from django.urls import reverse
from freezegun import freeze_time
from datetime import datetime, timedelta
from ..tests.tets_setup import TestSetUp, TestSetUpAlreadyCreatedModel
from rest_framework import status


class TestBombStartGameViews(TestSetUp):

    def test_start_game_without_data(self):
        response = self.client.post(
            self.start_bomb_game_url
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_correctly(self):
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_start_game_incorrect_min_bomb(self):
        self.bomb_game_data["bomb"] = 0
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_incorrect_max_bomb(self):
        self.bomb_game_data["bomb"] = 25
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_without_bomb(self):
        self.bomb_game_data.pop("bomb")
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_with_excess_money(self):
        self.bomb_game_data["start_sum"] = 99999999999999999999999
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_with_lack_money(self):
        self.bomb_game_data["start_sum"] = 0
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_witout_money(self):
        self.bomb_game_data.pop("start_sum")
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestBombStartGameAlreadyCreatedViews(TestSetUpAlreadyCreatedModel):

    def test_start_game_already_exists(self):
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    @freeze_time(datetime.now() + timedelta(hours=2))
    def test_start_game_after_time(self):
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
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
