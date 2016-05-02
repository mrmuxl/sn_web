#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^upload_bug/?$','kx.bug_report.views.upload_bug',name ='upload_bug'),
    url(r'^soft_bug/?$','kx.bug_report.views.soft_bug',name ='soft_bug'),
    url(r'^bug_log/?$','kx.bug_report.views.bug_log',name ='bug_log'),
)

