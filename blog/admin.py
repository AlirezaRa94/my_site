from django.contrib import admin

from blog import models


admin.site.register(models.Post)
admin.site.register(models.Author)
admin.site.register(models.Tag)
