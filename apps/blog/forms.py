#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import KxForumPosts,KxForumMpost,KxForumForum
from models import Blog

#attrs_dict = { 'class':'required' }
class Posts(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(Posts,self).__init__(*args,**kwargs)
        self.fields['title'] = forms.ChoiceFied(choices =[('','--------')] + [(f.title) for f in KxForumForum.objects.all()])
        #title = forms.CharField(choices=(),widget=forms.Select(attrs=arrts_dict))
    class Meta:
        posts = KxForumPosts
        fields = ('title', 'content')

class Mpost(forms.ModelForm):
    def save():
        pass
    class Meta:
        mpost = KxForumMpost
        #fields = ('title', 'content','create_time','update_time')
        
class Forums(forms.ModelForm):
    class Meta:
        forums = KxForumForum

class BlogForm(forms.ModelForm):
    class Meta:
        blogform = Blog

