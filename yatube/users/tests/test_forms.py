# users/tests/test_forms.py
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.forms import User

TEST_USERNAME = 'Username'
TEST_PASSWORD = 'flmfop8U'


class UserCreationFormTest(TestCase):
    def test_user_create_form(self):
        users_count = User.objects.count()
        form_data = {
            'username': TEST_USERNAME,
            'password1': TEST_PASSWORD,
            'password2': TEST_PASSWORD,
        }
        response = self.client.post(
            reverse('users:signup'),
            data=form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                username=TEST_USERNAME,
            ).exists()
        )
