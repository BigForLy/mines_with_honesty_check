from ..tests.tets_setup import TestSetUp
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

    def test_start_game_already_exists(self):
        # create game
        self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        # create already exists game
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_data
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
