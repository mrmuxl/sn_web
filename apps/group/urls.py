#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # url(r'^$','apps.group.views.login',name='login'),
    url(r'^user_remark/?$','apps.group.views.user_remark', name='user_remark'),
    url(r'^group_print/?$','apps.group.views.group_print', name='group_remark'),
)