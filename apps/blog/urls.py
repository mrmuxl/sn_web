#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','apps.blog.views.show',name ='show'),
    url(r'^show/?$','apps.blog.views.show',name ='show'),
    url(r'^help/?$','apps.blog.views.help',name ='help'),
    url(r'^index/?$','apps.blog.views.blog_index',name ='blog_index'),
)

