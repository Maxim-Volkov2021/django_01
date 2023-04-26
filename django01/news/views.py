import json

from django.core.paginator import Paginator
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from news.models import *


# Create your views here.
# def showAllNews(request):
#     news_list = News.objects.order_by(
#         "-timeCreate"
#     ).filter(
#         archive=False
#     ).prefetch_related(
#         'tags'
#     ).select_related(
#         'author'
#     )
#     paginator = Paginator(news_list, 10)
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         "title": "News",
#         "page_obj": page_obj
#     }
#     return render(request, 'news/index.html', context=context)

class ShowAllNews(ListView):
    model = News
    paginate_by = 10
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
                'author'
            )

def showNews(request, slugNews):
    try:
        news_item = News.objects.get(slug=slugNews)
        context = {
            "title": news_item.title,
            "news": news_item
        }
        return render(request, 'news/showNews.html', context=context)
    except:
        context = {
            "title": "Error",
            "text": "Error not found"
        }
        return render(request, 'news/showError.html', context=context, status=404)

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

def showTag(request, tag):
    news_list = News.objects.filter(
        tags__slug=tag
    ).order_by(
        "-timeCreate"
    ).prefetch_related(
        'tags'
    ).select_related(
        'author'
    )
    paginator = Paginator(news_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "title": f"News tag '{tag}'",
        "page_obj": page_obj
    }
    return render(request, 'news/index.html', context=context)

def showAllTags(request):
    tags_list = Tags.objects.all().order_by('name')
    paginator = Paginator(tags_list, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "title": f"Tags",
        "page_obj": page_obj,
        "name": 'tag'
    }
    return render(request, 'news/showLink.html', context=context)

def showAuthor(request, slugAuthor):
    news_list = News.objects.filter(
        author__slug=slugAuthor
    ).order_by(
        "-timeCreate"
    ).prefetch_related(
        'tags'
    ).select_related(
        'author'
    )
    paginator = Paginator(news_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "title": f"News author '{slugAuthor}'",
        "page_obj": page_obj
    }
    return render(request, 'news/index.html', context=context)

def showAllAuthors(request):
    author_list = Author.objects.all().order_by('slug')
    paginator = Paginator(author_list, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "title": f"Tags",
        "page_obj": page_obj,
        "name": 'author'
    }
    return render(request, 'news/showLink.html', context=context)

def pageNotFound(request, exception):
    context = {
        "title": "Error",
        "text": "Error not found"
    }
    return render(request, 'news/showError.html', context=context, status=404)
