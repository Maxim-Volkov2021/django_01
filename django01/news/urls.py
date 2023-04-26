from django.urls import path

from .views import *

urlpatterns = [
    path("", ShowAllNews.as_view(), name='home'),
    path("news/<slug:slugNews>", showNews, name='showNews'),
    path("author/<slug:slugAuthor>", showAuthor, name='showAuthor'),
    path("authors/", showAllAuthors, name='showAllAuthors'),
    path("tag/<slug:tag>", showTag, name='showTag'),
    path("tags/", showAllTags, name='showAllTags'),
    path("testwritedb/", testWriteDB),
]