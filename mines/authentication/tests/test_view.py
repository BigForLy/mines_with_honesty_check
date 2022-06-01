from .test_setup import TestSetUp
from datetime import datetime, timedelta
from rest_framework import status
import copy
from freezegun import freeze_time


class TestRegisterViews(TestSetUp):

    def test_user_can_register_without_data(self):
        response = self.client.post(
            self.signup_url
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        response = self.client.post(
            self.signup_url,
            self.user_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestLoginViews(TestSetUp):

    def setUp(self) -> None:
        super().setUp()
        self.client.post(
            self.signup_url,
            self.user_data,
            format="json"
        )

    def test_user_can_login_wthout_data(self):
        response = self.client.post(
            self.signin_url
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_correctly(self):
        response = self.client.post(
            self.signin_url,
            self.user_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_incorrect_data(self):
        data = copy.deepcopy(self.user_data)
        data['password'] += '1'

        response = self.client.post(
            self.signin_url,
            data,
            format="json"
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAccountUser(TestSetUp):

    def setUp(self):
        super().setUp()
        response = self.client.post(
            self.signup_url,
            self.user_data,
            format="json"
        )
        self.token = response.data['token']

    def test_user_profile_without_token(self):
        response = self.client.get(
            self.user_url
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_correctly(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.get(
            self.user_url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token)

    def test_user_profile_update_correctly(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        new_email = self.user_data['email'] + '1'
        data = copy.deepcopy(self.user_data)
        data['email'] = new_email

        response = self.client.put(
            self.user_url,
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], new_email)

    def test_user_profile_patch_correctly(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        new_email = self.user_data['email'] + '1'
        data = {"email": new_email}

        response = self.client.put(
            self.user_url,
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], new_email)


class TestTokenLiveCycle(TestSetUp):

    def setUp(self):
        super().setUp()
        response = self.client.post(
            self.signup_url,
            self.user_data,
            format="json"
        )
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    @freeze_time(datetime.now() + timedelta(hours=2))
    def test_token_live_cycle_ended(self):
        response = self.client.get(
            self.user_url
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_live_cycle_active(self):
        response = self.client.get(
            self.user_url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
