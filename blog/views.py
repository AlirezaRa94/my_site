from django.shortcuts import render
from django.urls.conf import path


def starting_page(request):
    return render(request, "blog/index.html")


def posts(request):
    pass


def post_details(request, post_name):
    pass
