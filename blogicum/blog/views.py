from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Post, Category
from .constants import POSTS_PER_PAGE


def get_published_posts():
    """Возвращает QuerySet опубликованных постов с оптимизацией."""
    return Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )


def index(request):
    template = 'blog/index.html'
    # Используем функцию и константу
    post_list = get_published_posts()[:POSTS_PER_PAGE]

    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    # Здесь тоже можно использовать функцию фильтрации,
    # но так как мы ищем по ID, достаточно добавить select_related
    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        pk=post_id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    # Используем функцию фильтрации для постов категории
    post_list = get_published_posts().filter(
        category=category
    )

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)
