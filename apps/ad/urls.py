#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','apps.ad.views.ad_list',name ='ad_list'),
    url(r'ad_list/?$','apps.ad.views.ad_list',name ='ad_list'),
)

