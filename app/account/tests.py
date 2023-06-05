from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Profile

User = get_user_model()


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_profile_creation(self):
        # Проверяем создание профиля
        url = '/api/account/profile/'
        data = {
            'date_birth': '2000-01-01',
            'place_residence': 'Test Residence',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().user, self.user)

    def test_profile_retrieval(self):
        # Проверяем получение профиля
        profile = Profile.objects.create(
            date_birth='2000-01-01',
            place_residence='Test Residence',
            user=self.user
        )
        url = f'/api/account/profile/{profile.pk}/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['date_birth'], '2000-01-01')
        self.assertEqual(response.data['place_residence'], 'Test Residence')

    def test_profile_update(self):
        # Проверяем обновление профиля
        profile = Profile.objects.create(
            date_birth='2000-01-01',
            place_residence='Test Residence',
            user=self.user
        )
        url = f'/api/account/profile/{profile.pk}/'
        data = {
            'date_birth': '1990-01-01',
            'place_residence': 'Updated Residence',
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['date_birth'], '1990-01-01')
        self.assertEqual(response.data['place_residence'], 'Updated Residence')

    def test_profile_deletion(self):
        # Проверяем удаление профиля
        profile = Profile.objects.create(
            date_birth='2000-01-01',
            place_residence='Test Residence',
            user=self.user
        )
        url = f'/api/account/profile/{profile.pk}/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Profile.objects.count(), 0)
