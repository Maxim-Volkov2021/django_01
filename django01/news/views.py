from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from .forms import *
from .models import *

from django.contrib.auth.decorators import login_required

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

@login_required
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
    slug_url_kwarg = 'tag'

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
    slug_url_kwarg = 'slugAuthor'

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


def addNews(request):
    try:
        author = Author.objects.filter(name__username=request.user.username).order_by('id')[0]
        if request.method == "POST":
            form = AddNewsForm(request.POST, request.FILES)
            if form.is_valid():
                # author = Author.objects.filter(name__username=request.user.username).order_by('id')[0]
                news = form.save(commit=False)
                news.author = author
                news.save()
                form.save_m2m()
                context = {
                    "title": "Success",
                    "text": "successfully added news"
                }
                return render(request, 'news/showError.html', context=context)
        else:
            form = AddNewsForm()
        return render(request, 'news/addNews.html', context={'form': form, 'title': "Add news"})
    except:
        context = {
            "title": "Error",
            "text": "You are not an author and cannot add news"
        }
        return render(request, 'news/showError.html', context=context)


def editNews(request, slugNews):
    try:
        author = Author.objects.filter(name__username=request.user.username).order_by('id')[0]
        if request.method == "POST":
            form = AddNewsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        else:
            news = (News.objects.filter(
                slug=slugNews
            ).prefetch_related(
                'tags'
            ).select_related(
                'author',
                'author__name'
            ))[0]
            form = AddNewsForm(instance=news)
            return render(request, 'news/addNews.html', context={'form': form, 'title': "Edit news"})
    except:
        context = {
            "title": "Error",
            "text": "You are not an author and cannot edit this news"
        }
        return render(request, 'news/showError.html', context=context)

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'news/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Register"
        return context

def ProfileUser(request):
    context = {
        "title": "Profile"
    }
    try:
        author = Author.objects.filter(name__username=request.user.username).order_by('id')[0]
        # context['author'] = True
        context['slugAuthor'] = author.slug
    except:
        pass

    return render(request, 'news/profileUser.html', context=context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def pageNotFound(request, exception):
    print(exception)
    context = {
        "title": "Error",
        "text": "Error not found"
    }
    return render(request, 'news/showError.html', context=context, status=404)
