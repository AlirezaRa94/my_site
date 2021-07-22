from django.shortcuts import render
from django.urls.conf import path


def starting_page(request):
    return render(request, 'blog/index.html')


def posts(request):
    return render(request, 'blog/posts.html')


def post_details(request, post_name):
    return render(request, 'blog/post_details.html')
