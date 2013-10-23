#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^my_issue/?$','apps.accounts.views.my_issue',name='my_issue'),
)