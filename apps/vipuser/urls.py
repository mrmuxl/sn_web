#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','apps.vipuser.views.vipuser_api',name='vipuser'),
    url(r'^vipuser_api/$','apps.vipuser.views.vipuser_api',name='vipuser'),
    url(r'^vipuser_test/(\w+)/(.+)/?$','apps.vipuser.views.vipuser_test',name='vipuser_test'),
)
