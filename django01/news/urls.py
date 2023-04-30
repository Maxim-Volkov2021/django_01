from django.urls import path

from .views import *

urlpatterns = [
    path("", ShowAllNews.as_view(), name='home'),
    path("news/<slug:slugNews>", ShowNews.as_view(), name='showNews'),
    path("author/<slug:slugAuthor>", ShowAuthor.as_view(), name='showAuthor'),
    path("authors/", ShowAllAuthors.as_view(), name='showAllAuthors'),
    path("tag/<slug:tag>", ShowTag.as_view(), name='showTag'),
    path("tags/", ShowAllTags.as_view(), name='showAllTags'),

    path("login/", LoginUser.as_view(), name='login'),
    path("logout/", logoutUser, name='logout'),
    path("register/", RegisterUser.as_view(), name='register'),
    path("accounts/profile/", ProfileUser, name='profileUser'),


    path("news/add/", addNews, name='addNews'),
    path("news/<slug:slugNews>/edit/", editNews, name='editNews'),
    path("testwritedb/", testWriteDB),
]