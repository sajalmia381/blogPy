from django import forms
from .models import Article, Author, Comment, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class Create_post(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'body',
            'image',
            'category'
        ]

class User_creation(UserCreationForm):
    class Meta:
        model = User
        fields=[
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        ]

class Author_user(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'details',
            'author_picture'
        ]

class Single_post_comment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {
            'name',
            'email',
            'post_comment'
        }
class Create_category(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name'
        ]