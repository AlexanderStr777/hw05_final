# posts/tests/test_models.py
from django.test import TestCase

from ..models import Comment, Follow, Group, Post, User

USERNAME = 'user'
USERNAME_1 = 'user1'
TEST_GROUP_TITLE = 'Тестовая группа'
TEST_GROUP_SLUG = 'slug'
TEST_GROUP_DESCRIPTION = 'Test description'
TEST_POST_TEXT = 'Test post in test group'
TEST_COMMENT = 'Test comment on test post'


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)
        cls.user1 = User.objects.create_user(username=USERNAME_1)
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
            description=TEST_GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=TEST_POST_TEXT,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user1,
            text=TEST_COMMENT
        )
        cls.follow = Follow.objects.create(
            user=cls.user1,
            author=cls.user
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        self.assertEqual(str(post), TEST_POST_TEXT[:15])

        group = PostModelTest.group
        self.assertEqual(str(group), TEST_GROUP_TITLE)

        comment = PostModelTest.comment
        author = comment.author
        self.assertEqual(
            str(comment),
            f'Комментарий пользователя {author}: {TEST_COMMENT[:15]}'
        )

        follow = PostModelTest.follow
        self.assertEqual(
            str(follow),
            (f'подписка пользователя {PostModelTest.user1} '
             f'на пользователя {PostModelTest.user}')
        )
