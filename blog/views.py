from django.views.generic import ListView, DetailView

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


class PostDetailView(DetailView):
    template_name = 'blog/post_details.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_tags'] = self.object.tags.all()
        context['comment_form'] = CommentForm()
        return context
