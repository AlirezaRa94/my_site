from django.contrib import admin

from blog import models


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'date')
    list_filter = ('author', 'tags', 'date')


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Author)
admin.site.register(models.Tag)
