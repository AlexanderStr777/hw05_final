# posts/models.py
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Группа постов'
        verbose_name_plural = 'Группы постов'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('Содержание', help_text='Содержание поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='group',
        blank=True,
        null=True,
        verbose_name='Сообщество',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий пользователя {self.author}: {self.text[:15]}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    def save(self, *args, **kwargs):
        existing = Follow.objects.filter(
            user=self.user,
            author=self.author
        ).exists()
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на самого себя')
        if existing:
            raise ValidationError('Такая подписка уже существует')
        super(Follow, self).save(*args, **kwargs)

    def __str__(self):
        return (f'подписка пользователя {self.user} '
                f'на пользователя {self.author}')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
