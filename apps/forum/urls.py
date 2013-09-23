#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^index/?$','apps.forum.views.index',name ='forum_index'),

)

