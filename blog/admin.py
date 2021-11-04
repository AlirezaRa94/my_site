from django.contrib import admin

from blog import models


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'date')
    list_filter = ('author', 'tags', 'date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'post')
    list_filter = ('post',)


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Author)
admin.site.register(models.Tag)
admin.site.register(models.Comment, CommentAdmin)
