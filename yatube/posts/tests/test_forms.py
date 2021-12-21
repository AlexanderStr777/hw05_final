# posts/tests/test_forms.py
import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
POST_CREATE_URL = 'posts:post_create'
POST_EDIT_URL = 'posts:post_edit'
ADD_COMMENT_URL = 'posts:add_comment'
TEST_USERNAME = 'HasNoName'
TEST_GROUP_TITLE = 'Test Group 1'
TEST_GROUP_SLUG = 'test1'
TEST_GROUP_DESCRIPTION = 'Test Group 1'
TEST_POST_TEXT = 'Test text 1'
TEST_POST_TEXT_UPDATE = 'Test text 1 Update'
TEST_POST_TEXT_2 = 'Test text 2'
TEST_POST_IMG_URL = 'posts/small.gif'
TEST_COMMENT = 'Test comment'
TEST_IMG = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00'
    b'\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
    b'\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
TEST_IMAGE_UPLOADE = SimpleUploadedFile(
    name='small.gif',
    content=TEST_IMG,
    content_type='image/gif'
)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.group_1 = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
            description=TEST_GROUP_DESCRIPTION
        )
        cls.post_1 = Post.objects.create(
            text=TEST_POST_TEXT,
            author=cls.user,
            group=cls.group_1
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Проверка работы формы создания поста"""
        posts_count = Post.objects.count()
        form_data = {
            'text': TEST_POST_TEXT_2,
            'group': PostFormTest.group_1.id,
            'image': TEST_IMAGE_UPLOADE
        }
        self.authorized_client.post(
            reverse(POST_CREATE_URL),
            data=form_data
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=TEST_POST_TEXT_2,
                author=PostFormTest.user,
                group=PostFormTest.group_1,
                image=TEST_POST_IMG_URL
            ).exists()
        )

    def test_post_edit(self):
        """Проверка работы формы изменения поста"""
        form_data = {
            'text': TEST_POST_TEXT_UPDATE,
            'group': PostFormTest.group_1.id
        }
        response = self.authorized_client.post(
            reverse(POST_EDIT_URL, args=[1]),
            form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        PostFormTest.post_1.refresh_from_db()
        self.assertEqual(PostFormTest.post_1.text, TEST_POST_TEXT_UPDATE)


class CommentFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
            description=TEST_GROUP_DESCRIPTION
        )
        cls.post = Post.objects.create(
            text=TEST_POST_TEXT,
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.unauthorized_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_comment(self):
        """Проверка работы формы создания комментария"""
        post_comments_count = CommentFormTest.post.comments.count()
        form_data = {
            'text': TEST_COMMENT,
        }
        self.authorized_client.post(
            reverse(ADD_COMMENT_URL, args=[1]),
            data=form_data
        )
        self.assertEqual(
            CommentFormTest.post.comments.count(),
            post_comments_count + 1
        )
        self.assertTrue(
            Comment.objects.filter(
                text=TEST_COMMENT,
                author=CommentFormTest.user,
                post=CommentFormTest.post
            ).exists()
        )

    def test_create_comment_unauthorized_user(self):
        """Проверка невозможности создания комментария
        неавторизированным пользователем"""
        post_comments_count = CommentFormTest.post.comments.count()
        form_data = {
            'text': TEST_COMMENT,
        }
        self.unauthorized_client.post(
            reverse(ADD_COMMENT_URL, args=[1]),
            data=form_data
        )
        self.assertEqual(
            CommentFormTest.post.comments.count(),
            post_comments_count
        )
        self.assertFalse(
            Comment.objects.filter(
                text=TEST_COMMENT,
                author=CommentFormTest.user,
                post=CommentFormTest.post
            ).exists()
        )
