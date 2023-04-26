from django.contrib import admin

from .models import *


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('tags',)

class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(News, NewsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Author)

