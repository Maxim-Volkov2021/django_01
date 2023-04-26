from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_author_name', 'get_html_photo', 'timeCreate', 'archive')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('tags', 'author', 'timeCreate')
    list_editable = ('archive',)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('tags',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img style='width:10%' src='{object.photo.url}'>")
    get_html_photo.short_description = "photo"
    def get_author_name(self, object):
        if object.author.name.first_name or object.author.name.last_name:
            return object.author.name.first_name + " " + object.author.name.last_name
        else:
            return object.author.name.username

    get_author_name.short_description = "author"


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class AuthorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_author_name', 'get_author_username', 'slug')
    list_display_links = ('id', 'get_author_name', 'get_author_username', 'slug')
    search_fields = ('name__first_name', 'name__last_name', 'name__username')

    def get_author_name(self, object):
        if object.name.first_name or object.name.last_name:
            return object.name.first_name + " " + object.name.last_name
    get_author_name.short_description = "name"

    def get_author_username(self, object):
        if object.name.username:
            return object.name.username
    get_author_username.short_description = "username"


admin.site.register(News, NewsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Author, AuthorsAdmin)

