from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class AddNewsForm(forms.ModelForm):
    # title = forms.CharField(max_length=200)
    # slug = forms.SlugField(max_length=200)
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'row': 10}))
    # tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all())
    # archive = forms.BooleanField(required=False)
    class Meta:
        model = News
        fields = ['title', 'slug', 'photo', 'content', 'tags', 'archive']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 60, 'row': 10})
        }


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
