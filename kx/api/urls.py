#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^record/$','kx.api.views.record'),
    url(r'^lan_record/$','kx.api.views.lan_record'),
    url(r'^pub_record/$','kx.api.views.pub_record'),
    url(r'^utime/$','kx.api.views.utime'),
    url(r'^cadd/$','kx.api.views.cadd'),
    url(r'^uninstall/$','kx.api.views.uninstall'),
    url(r'^tongji/$','kx.views.tongji',name='tongji'),
    url(r'^login_tongji/$','kx.views.login_tongji',name='login_tongji'),


)

