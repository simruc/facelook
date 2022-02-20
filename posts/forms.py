from dataclasses import fields
import imp
from charset_normalizer import models
from django import forms
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message','images']


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']