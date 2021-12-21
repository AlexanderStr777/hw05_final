# posts/views.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post

User = get_user_model()


# Главная страница
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGINATOR_VALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    title = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, 'posts/index.html', context)


# Cтраницы, на которых будут посты, отфильтрованные по группам
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    post_list = group.group.all()
    paginator = Paginator(post_list, settings.PAGINATOR_VALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


# Страницы пользователя
def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, settings.PAGINATOR_VALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user,
            author=author,
        ).exists()
    else:
        following = False

    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


# Страница записи
def post_detail(request, post_id):
    form = CommentForm()
    post = Post.objects.get(id=post_id)
    author = post.author
    title = post.text[:31]
    context = {
        'post': post,
        'author': author,
        'title': title,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


# Страницы создания поста
@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()

        return redirect(
            reverse('posts:profile', args=[request.user.username]),
        )

    return render(request, 'posts/create_post.html', {'form': form})


# Страница редактирования поста
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


# Добавление комментария
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    # ...
    title = 'Ваша лента авторов'
    user_following = Follow.objects.filter(user=request.user)
    authors = [i.author for i in user_following]
    post_list = Post.objects.filter(author__in=authors)
    paginator = Paginator(post_list, settings.PAGINATOR_VALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    following = Follow.objects.filter(
        user=request.user,
        author=author,
    ).exists()
    if author != request.user:
        if not following:
            Follow.objects.create(
                user=request.user,
                author=author
            )
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(
        user=request.user,
        author=author
    ).delete()
    return redirect('posts:profile', username=username)
