#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','apps.forum.views.index',name ='forum_index'),
    url(r'^index/?$','apps.forum.views.index',name ='forum_index'),
    url(r'^add/?$','apps.forum.views.add',name ='forum_add'),

)

