#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^index/?$', TemplateView.as_view(template_name="user/index.html")),
    url(r'^friend/?$', TemplateView.as_view(template_name="user/friend.html")),
    url(r'^info/?$', TemplateView.as_view(template_name="user/info.html")),
    url(r'^friendAdd/?$', TemplateView.as_view(template_name="user/friend_add.html")),
    url(r'^printer/auth/?$', TemplateView.as_view(template_name="user/printer_auth.html")),
)