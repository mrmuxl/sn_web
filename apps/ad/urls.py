#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$','apps.ad.views.ad_list',name ='ad_list'),
    url(r'ad_list/?$','apps.ad.views.ad_list',name ='ad_list'),
    url(r'getAdList/?$','apps.ad.views.ad_api'),
    url(r'operator/add/?$',TemplateView.as_view(template_name="ad/operator_add_form.html")),
)

