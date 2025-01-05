from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post, User

PAGINATE_COUNT: int = 10


def get_general_posts_filter() -> QuerySet[Any]:
    """Фильтр для постов со счётчиком комментариев и сортировкой."""
    return Post.objects.select_related(
        'author',
        'location',
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


class EditContentMixin(LoginRequiredMixin):
    """
    Добавляет проверку авторства для редактирования и удаления.
    Если проверка провалена, то возвращает на страницу поста.
    """

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if self.get_object().author != request.user:
            return redirect(
                'blog:post_detail',
                post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class ValidationMixin:
    """
    Валидидатор формы.
    Устанавливает пользователя в качестве автора.
    """

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RedirectionPostMixin:
    """После выполнения перенаправит на страницу поста."""

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class RedirectionProfileMixin:
    """После выполнения перенаправит на страницу профиля."""

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class PostMixin:
    """Базовый миксин для постов."""

    model = Post


class PostFormMixin(PostMixin):
    """Миксин для постов с формой."""

    form_class = PostForm


class PostListMixin(PostMixin):
    """Миксин для страниц со списком постов и пагинацией."""

    paginate_by = PAGINATE_COUNT
