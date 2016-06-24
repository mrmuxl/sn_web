#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','apps.vipuser.views.vipuser_api',name='vip_user'),
)
