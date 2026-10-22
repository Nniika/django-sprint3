from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).order_by('-pub_date')[:5]
    
    context = {'posts': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post,
        pk=post_id,
        is_published=True,
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
    post_list = category.post_set.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    
    context = {
        'category': category,
        'posts': post_list,
    }
    return render(request, template, context)
