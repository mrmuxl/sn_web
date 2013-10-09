#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
    url(r'^$','apps.operator.views.index',name ='operator_index'),
)

