#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^add/?$','apps.spool.views.spool_add',name ='spool_add'),
    url(r'^select/?$','apps.spool.views.spool_select',name ='spool_select'),
    url(r'^update/?$','apps.spool.views.spool_update',name ='spool_update'),
)

