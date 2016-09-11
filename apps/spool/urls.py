#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^add/?$','apps.spool.views.spool_add',name ='spool_add'),
)

