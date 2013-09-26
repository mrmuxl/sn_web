#_*_coding:utf-8_*_

from django import forms
from models import Forum

class ForumForm(forms.Form):
    class Meta:
        f = Forum

