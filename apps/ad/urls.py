#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$','apps.ad.views.ad_list',name ='ad_list'),
    url(r'ad_list/?$','apps.ad.views.ad_list',name ='ad_list'),
    url(r'getAdList/?$','apps.ad.views.ad_api'),
    url(r'operator_select/?$','apps.ad.views.operator_select'),
    url(r'operator_show/?$','apps.ad.views.operator_show'),
    url(r'operator/add/?$','apps.ad.views.operator_add',name='apps.ad.views.operator_add'),
)

