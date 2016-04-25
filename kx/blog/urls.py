#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','kx.blog.views.show',name ='show'),
    url(r'^show/$','kx.blog.views.show',name ='show'),
)

