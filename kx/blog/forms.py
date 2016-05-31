#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import KxForumPosts,KxForumMpost,KxForumForum

class Posts(forms.ModelForm):
    class Meta:
        posts = KxForumPosts
        fields = ('title', 'content')

class Mpost(forms.ModelForm):
        mpost = KxForumMpost
        #fields = ('title', 'content','create_time','update_time')

class Forums(forms.ModelForm):
    class Meta:
        forums = KxForumForum
