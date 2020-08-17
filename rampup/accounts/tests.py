import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .serializers import RegisterSerializer, UserSerializer
from .models import User


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"name": "testing", "email": "test@jtg.com",
                "password": "test123123", "city": "testcity", "state": "teststate"}
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="testy@jtg.com", name="testing", 
                password="test123123")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_user_retrieve(self):
        response = self.client.get(reverse("users-detail", kwargs={"pk": 1}))
        print(response.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["email"], "testing")

