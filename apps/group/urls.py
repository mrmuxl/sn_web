#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # url(r'^$','apps.group.views.login',name='login'),
    url(r'^user_remark/?$','apps.group.views.user_remark', name='user_remark'),
    url(r'^list_print/?$','apps.group.views.list_print', name='list_print'),
    url(r'^save_print/?$','apps.group.views.save_print', name='save_print'),
    url(r'^del_print/?$','apps.group.views.del_print', name='del_print'),
    url(r'^add_user/?$','apps.group.views.add_user', name='group_add_user'),
)