from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Author(models.Model):
    name = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name="URL"
    )

    def __str__(self):
        return self.slug

    def get_absolut_url(self):
        return reverse("showAuthor", kwargs={"slugAuthor": self.slug})


class Tags(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name="URL")

    def get_absolut_url(self):
        return reverse("showTag", kwargs={"tag": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name="URL"
    )
    content = models.TextField(blank=False)
    photo = models.ImageField(upload_to="photos/%Y/%m")
    tags = models.ManyToManyField(Tags)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True
    )
    timeCreate = models.DateTimeField(auto_now_add=True)
    timeUpdate = models.DateTimeField(auto_now=True)
    archive = models.BooleanField(default=False)

    def get_absolut_url(self):
        return reverse("showNews", kwargs={"slugNews": self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


