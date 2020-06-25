from django.contrib.auth.models import User
from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.users = baker.make('auth.User', _quantity=3)
        self.test_user = User.objects.create(username="test", password="1111")
        self.test_user.set_password(raw_password="1111")
        self.test_user.save()
        self.data = {"username": "test", "password": "1111"}

    def test_should_list_user(self):
        """
        All user list
        Request : GET - /api/user/
        """
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for user_response, user in zip(response.data, self.users):
            self.assertEqual(user_response['id'], user.id)
            self.assertEqual(user_response['username'], user.username)

    def test_should_detail_user(self):
        """
        User detail
        Request : GET - /api/user/{user_id}
        """
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/user/{user.id}')
        user_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_response.id, user.id)
        self.assertEqual(user_response.username, user.username)

    def test_should_create_user(self):
        """
        Request : POST - /api/user/
        """
        data = {"username": "newuser", "password": "1111"}
        response = self.client.post('/api/user/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, data['username'])

    def test_should_delete_user(self):
        """
        Request : DELETE - /api/user/{user_id}
        """
        user = self.users[0]
        self.client.force_authenticate(user=user)
        entry = User.objects.get(id=user.id)
        response = self.client.delete(f'/api/user/{entry.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=entry.id).exists())

    def test_should_update_user(self):
        """
        Request : PATCH - /api/user/{user_id}
        """
        user = self.users[0]
        prev_name = user.username
        self.client.force_authenticate(user=user)
        data = {"username": "changed"}
        response = self.client.patch(f'/api/user/{user.id}', data=data)
        user_response = Munch(response.data)
        self.assertNotEqual(user_response.username, prev_name)

    def test_should_login(self):
        """
        Request : POST - /api/user/login
        """
        response = self.client.post('/api/user/login', data=self.data)
        user_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user_response.token)
        self.assertTrue(Token.objects.filter(key=user_response.token).exists())

    def test_logout(self):
        """
        Request : DELETE - /api/user/logout
        """
        response = self.client.post('/api/user/login', data=self.data)
        token = response.data['token']
        self.client.force_authenticate(user=self.test_user, token=token)
        response = self.client.delete('/api/user/logout', HTTP_AUTHORIZATION='Token '+token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(pk=token).exists())
