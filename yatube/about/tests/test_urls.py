# about/tests/test_urls.py
from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def about_author(self):
        """Страница об авторе доступна всем"""
        response = self.guest_client.get('about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def about_tech(self):
        """Страницы о технологиях доступнав всем"""
        response = self.guest_client.get('about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
