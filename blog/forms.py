from django import forms

from blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            "first_name": "Your First Name",
            "last_name": "Your Last Name",
            "email": "Your Email",
            "text": "Your Comment"
        }
