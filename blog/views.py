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
    def is_stored_post(request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def render_post_details(self, request, post, comment_form):
        comments = post.comments.all().order_by('-id')
        tags = post.tags.all()
        is_saved_for_later = self.is_stored_post(request, post_id=post.id)
        context = {
            'post': post,
            'post_tags': tags,
            'comment_form': comment_form,
            'comments': comments,
            'saved_for_later': is_saved_for_later,
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


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = dict()

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored_posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
