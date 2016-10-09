#_*_coding:utf-8_*_

from django import forms
from models import ForumPost

class ForumPostForm(forms.Form):
    class Meta:
        f = ForumPost

