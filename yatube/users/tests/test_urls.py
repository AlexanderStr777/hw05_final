# users/tests/test_urls.py
from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from users.forms import User


class UserUrlTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url_accessing(self):
        "Проверка доступности страниц"
        urls = (
            'users:logout',
            'users:signup',
            'users:login',
            'users:password_reset_form'
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(reverse(url))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'users:logout': 'users/logged_out.html',
            'users:login': 'users/login.html',
            'users:signup': 'users/signup.html'
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(reverse(adress))
                self.assertTemplateUsed(response, template)
