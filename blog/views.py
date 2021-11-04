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

    @staticmethod
    def render_post_details(request, post, comment_form):
        comments = post.comments.all().order_by('-id')
        tags = post.tags.all()
        context = {
            'post': post,
            'post_tags': tags,
            'comment_form': comment_form,
            'comments': comments
        }
        return render(request, 'blog/post_details.html', context)

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm()
        return self.render_post_details(request, post, comment_form)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-details-page", args=[slug]))

        return self.render_post_details(request, post, comment_form)
