#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','kx.tongji.views.tongji',name='tongji'),
    url(r'^tongji/$','kx.tongji.views.tongji',name='tongji'),
    url(r'^record/?$','kx.api.views.record'),
    url(r'^lan_record/?$','kx.api.views.lan_record'),
    url(r'^pub_record/?$','kx.api.views.pub_record'),
    url(r'^utime/?$','kx.api.views.utime'),
    url(r'^Uninstall/?$','kx.api.views.uninstall'),
    url(r'^send_diskfree_email/?$','kx.api.views.send_diskfree_email'),
    url(r'^login_tongji/$','kx.tongji.views.login_tongji',name='login_tongji'),
    url(r'^reg_tongji/?$','kx.tongji.views.reg_tongji',name='reg_tongji'),
)

urlpatterns += patterns('',
    url(r'^remain_ratio_chart/?$','kx.tongji.views.remain_ratio_chart',name='remain_ratio_chart'),
    url(r'^silence_ratio_chart/?$','kx.tongji.views.silence_ratio_chart',name='silence_ratio_chart'),
    url(r'^lan_line_chart/?$','kx.tongji.views.lan_line_chart',name='lan_line_chart'),
    url(r'^lan_stack_chart/?$','kx.tongji.views.lan_stack_chart',name='lan_stack_chart'),
    url(r'^online_act_chart/?$','kx.tongji.views.online_act_chart',name='online_act_chart'),
    url(r'^uninstall_chart/?$','kx.tongji.views.uninstall_chart',name='uninstall'),
    url(r'^reg_chart/?$','kx.tongji.views.reg_chart',name='reg_chart'),
    url(r'^bug_chart/?$','kx.tongji.views.bug_chart',name='bug_chart'),
    url(r'^bug_ratio_chart/$','kx.tongji.views.bug_ratio_chart',name='bug_ratio_chart'),

)
urlpatterns += patterns('',
    url(r'^bug_msg/?$','kx.tongji.views.bug_msg',name='bug_msg'),
    url(r'^bug_log/?$','kx.tongji.views.bug_log',name='bug_log'),

)
