from django.shortcuts import render, get_object_or_404

from blog.models import Post


def starting_page(request):
    latest_posts = Post.objects.all().order_by('-date')[:3]
    return render(request, 'blog/index.html', {
        "latest_posts": latest_posts
    })


def posts(request):
    sorted_posts = Post.objects.all().order_by('-date')
    return render(request, 'blog/posts.html', {
        "all_posts": sorted_posts
    })


def post_details(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_details.html', {
        "post": identified_post
    })
