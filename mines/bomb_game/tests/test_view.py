from ..tests.tets_setup import TestStartGameSetUp, TestSetUpAlreadyCreatedModel, TestMoveGameSetUp
from rest_framework import status


class TestBombStartGameViews(TestStartGameSetUp):

    def test_start_game_without_data(self):
        response = self.client.post(
            self.start_bomb_game_url
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_correctly(self):
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_start_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_start_game_incorrect_min_bomb(self):
        self.bomb_game_start_data["bomb"] = 0
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_start_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_incorrect_max_bomb(self):
        self.bomb_game_start_data["bomb"] = 25
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_start_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_without_bomb(self):
        self.bomb_game_start_data.pop("bomb")
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_start_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_with_excess_money(self):
        self.bomb_game_start_data["start_sum"] = 99999999999999999999999
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_start_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_with_lack_money(self):
        self.bomb_game_start_data["start_sum"] = 0
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_start_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_game_witout_money(self):
        self.bomb_game_start_data.pop("start_sum")
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_start_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestBombStartGameAlreadyCreatedViews(TestSetUpAlreadyCreatedModel):

    def test_start_game_already_exists(self):
        response = self.client.post(
            self.start_bomb_game_url,
            self.bomb_game_start_data
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class TestBombMoveGameNoCreatedViews(TestStartGameSetUp):

    def test_move_game_without_data(self):
        response = self.client.post(
            self.move_bomb_game_url
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestBombMoveGameViews(TestMoveGameSetUp):

    def test_move_game_without_data(self):
        response = self.client.post(
            self.move_bomb_game_url
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_game_correctly(self):
        response = self.client.post(
            self.move_bomb_game_url,
            self.bomb_game_move_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_move_game_incorrect_min_move(self):
        self.bomb_game_move_data["move"] = -1
        response = self.client.post(
            self.move_bomb_game_url,
            self.bomb_game_move_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_game_incorrect_max_move(self):
        self.bomb_game_move_data["move"] = 26
        response = self.client.post(
            self.move_bomb_game_url,
            self.bomb_game_move_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_game_duplicate(self):
        response = self.client.post(
            self.move_bomb_game_url,
            self.bomb_game_move_data
        )
        # проверяем что ход успешный
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            self.move_bomb_game_url,
            self.bomb_game_move_data
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_move_game_lose(self):
        self.bomb_game_move_data["move"] = 1
        response = self.client.post(
            self.move_bomb_game_url,
            self.bomb_game_move_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("bomb_in")),
                         self.bomb_game_start_data.get("bomb"))
