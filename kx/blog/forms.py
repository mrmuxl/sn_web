#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import KxForumPosts 

class AddPost(forms.ModelForm):
    class Meta:
        add_post = KxForumPosts
        fields = ('title', 'content')
