import json

from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from news.models import *


# Create your views here.
class ShowAllNews(ListView):
    model = News
    paginate_by = 5
    template_name = "news/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "News"
        return context

    def get_queryset(self):
        return News.objects.order_by(
                "-timeCreate"
            ).filter(
                archive=False
            ).prefetch_related(
                'tags'
            ).select_related(
                'author',
                'author__name'
            )

class ShowNews(DetailView):
    model = News
    template_name = "news/showNews.html"
    context_object_name = 'news'
    slug_url_kwarg = 'slugNews'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["news"].title
        return context

    def get_queryset(self):
        return News.objects.filter(slug=self.kwargs['slugNews'], archive=False).select_related('author__name')

def testWriteDB(request):
    # n = news.objects.all()
    # n.delete()
    # return HttpResponse("test delete DB")
    # for i in range(5):
    #     for j in range(2):
    #         n = news()
    #         n.title = "test title"
    #         n.content = "test content"
    #         n.tags = [
    #             (j+i)
    #         ]
    #         n.save()
    #         print(n)
    #
    # l = "abcdefg"
    # for i in range(5):
    #     t = tags()
    #     t.name = l[i]
    #     t.save()
    #     print(t)
    # t = Tags.objects.all()
    # for temp in t:
    #     temp.name = f'test{time.time()}'
    #     temp.save()

    return HttpResponse("test write DB")


class ShowTag(ListView):
    model = News
    paginate_by = 5
    template_name = "news/index.html"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"News tag '{self.kwargs['tag']}'"
        return context

    def get_queryset(self):
        return News.objects.filter(
            tags__slug=self.kwargs['tag']
        ).order_by(
            "-timeCreate"
        ).prefetch_related(
            'tags'
        ).select_related(
            'author',
            'author__name'
        )

class ShowAllTags(ListView):
    model = Tags
    paginate_by = 10
    template_name = "news/showLink.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Tags"
        context["name"] = "tag"
        return context

    def get_queryset(self):
        return Tags.objects.all().order_by('name')


class ShowAuthor(ListView):
    model = News
    paginate_by = 5
    template_name = "news/index.html"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['page_obj'][0].author.name.first_name or context['page_obj'][0].author.name.last_name:
            context["title"] = f"News author '{context['page_obj'][0].author.name.first_name} {context['page_obj'][0].author.name.last_name}'"
        else:
            context["title"] = f"News author '{context['page_obj'][0].author.name.username}'"
        return context

    def get_queryset(self):
        return News.objects.filter(
            author__slug=self.kwargs['slugAuthor']
        ).order_by(
            "-timeCreate"
        ).prefetch_related(
            'tags'
        ).select_related(
            'author',
            'author__name'
        )


class ShowAllAuthors(ListView):
    model = Author
    paginate_by = 10
    template_name = "news/showLink.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Authors"
        context["name"] = "author"
        return context

    def get_queryset(self):
        return Author.objects.all().order_by('slug').select_related('name')

def pageNotFound(request, exception):
    context = {
        "title": "Error",
        "text": "Error not found"
    }
    return render(request, 'news/showError.html', context=context, status=404)
