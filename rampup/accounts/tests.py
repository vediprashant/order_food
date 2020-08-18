import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts import( 
    models as accounts_models,
    serializers as accounts_serializers,
)


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"name": "testing", "email": "test@jtg.com",
                "password": "test123123", "city": "testcity", "state": "teststate"}
        response = self.client.post("/accounts/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = accounts_models.User.objects.create_user(email="testy@jtg.com", name="testing", 
                password="test123123", city="testcity", state="teststate")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key, content_type="application/json")
        
    def test_user_retrieve(self):
        response = self.client.get(reverse('users-detail', kwargs={"pk":self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "testy@jtg.com")

    def test_user_update_by_owner(self):
        response = self.client.put(reverse('users-detail', kwargs={"pk": self.user.id}),
                                   {"name": "testing", "email": "test@jtg.com",
                "password": "test123123", "city": "testcityy", "state": "teststate"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_by_random_user(self):
        random_user = accounts_models.User.objects.create_user(email="tasty@jtg.com", name="testing", 
                password="test123123", city="testcity", state="teststate")
        self.client.force_authenticate(user=random_user)
        response = self.client.put(reverse("users-detail", kwargs={"pk": self.user.id}),
                                   {"name": "testing", "email": "test@jtg.com",
                "password": "test123123", "city": "testcityyy", "state": "teststate"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_user_delete(self):
        response = self.client.delete(reverse('users-detail', kwargs={"pk": self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
