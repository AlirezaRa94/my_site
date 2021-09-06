from django.core.validators import MinLengthValidator
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=80)
    email_address = models.EmailField()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name()


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=256)
    image_name = models.CharField(max_length=128)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='posts')
    tags = models.ManyToManyField(Tag)
