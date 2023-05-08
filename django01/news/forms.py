from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class AddNewsForm(forms.ModelForm):
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
