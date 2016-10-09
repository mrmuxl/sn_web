#_*_coding:utf-8_*_

from django.forms import ModelForm
from models import ForumPost,ForumComment

class ForumPostForm(ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content',]

class ForumCommentForm(ModelForm):
    class Meta:
        model = ForumComment
        fields = ['fid','content']
