# posts/tests/test_urls.py
from http import HTTPStatus

from django.test import Client, TestCase

from posts.models import Group, Post, User


class PostURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )
        Group.objects.create(
            title='Test Group',
            slug='test',
            description='Test Group',
        )

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url_accessing(self):
        "Проверка доступности страниц"
        urls = (
            '/',
            '/group/test/',
            '/profile/HasNoName/',
            '/posts/1/',
            '/posts/1/edit/',
            '/create/',
            '/follow/'
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_page(self):
        """Проверка ответа несуществующей страницы"""
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/follow/': 'posts/follow.html',
            '/group/test/': 'posts/group_list.html',
            '/profile/HasNoName/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            '/posts/1/edit/': 'posts/create_post.html'
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
