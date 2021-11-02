from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from blog.forms import CommentForm
from blog.models import Post


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date', 'title']
    context_object_name = 'latest_posts'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs[:3]


class PostListView(ListView):
    template_name = 'blog/posts.html'
    model = Post
    ordering = ['-date', 'title']
    context_object_name = 'all_posts'


class PostDetailView(View):
    template_name = 'blog/post_details.html'

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': CommentForm()
        }
        return render(request, 'blog/post_details.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-details-page", args=[slug]))

        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': comment_form
        }
        return render(request, 'blog/post_details.html', context)
