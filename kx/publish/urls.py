#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','kx.publish.views.publish_index',name ='publish_index'),
    url(r'add/?$','kx.publish.views.publish_index',name ='publish_add'),
    url(r'edit/?$','kx.publish.views.publish_index',name ='publish_edit'),
)

