#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # url(r'^$','apps.group.views.login',name='login'),
    url(r'^user_remark/?$','apps.group.views.user_remark', name='user_remark'),
    url(r'^list_print/?$','apps.group.views.list_print', name='list_print'),
    url(r'^save_print/?$','apps.group.views.save_print', name='save_print'),
    url(r'^del_print/?$','apps.group.views.del_print', name='del_print'),
    url(r'^add_user/?$','apps.group.views.add_user', name='group_add_user'),
    url(r'^go_auth/?$','apps.group.views.go_auth', name='group_go_auth'),
    url(r'^my_auth/?$','apps.group.views.my_auth', name='group_my_auth'),
    url(r'^list_auth/?$','apps.group.views.list_auth', name='group_list_auth'),
    url(r'^deal_auth/?$','apps.group.views.deal_auth', name='group_deal_auth'),
    url(r'^group_list/?$','apps.group.views.group_list', name='group_group_list'),
    url(r'^group_add/?$','apps.group.views.group_add', name='group_group_add'),
    url(r'^group_user/?$','apps.group.views.group_user', name='group_group_user'),
    url(r'^guser_add/?$','apps.group.views.guser_add', name='group_guser_add'),
    url(r'^guser_del/?$','apps.group.views.guser_del', name='group_guser_del'),
    url(r'^print_share/?$','apps.group.views.print_share', name='group_print_share'),
    url(r'^guser_remark/?$','apps.group.views.guser_remark', name='group_guser_remark'),
)