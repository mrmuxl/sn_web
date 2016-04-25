#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^record/?$','kx.api.views.record'),
    url(r'^lan_record/?$','kx.api.views.lan_record'),
    url(r'^pub_record/?$','kx.api.views.pub_record'),
    url(r'^utime/?$','kx.api.views.utime'),
    url(r'^cadd/?$','kx.api.views.cadd'),
    url(r'^uninstall/?$','kx.api.views.uninstall'),
    url(r'^$','kx.tongji.views.tongji',name='tongji'),
    url(r'^tongji/$','kx.tongji.views.tongji',name='tongji'),
    url(r'^login_tongji/$','kx.tongji.views.login_tongji',name='login_tongji'),
    url(r'^uninstall_chart/$','kx.tongji.views.uninstall_chart',name='uninstall'),
    url(r'^bug_chart/$','kx.tongji.views.bug_chart',name='bug_chart'),
    url(r'^bug_msg/$','kx.tongji.views.bug_msg',name='bug_msg'),
    url(r'^bug_log/$','kx.tongji.views.bug_log',name='bug_log'),
    url(r'^bug_ratio_chart/$','kx.tongji.views.bug_ratio_chart',name='bug_ratio_chart'),
    url(r'^remain_ratio_chart/$','kx.tongji.views.remain_ratio_chart',name='remain_ratio_chart'),
    url(r'^silence_ratio_chart/$','kx.tongji.views.silence_ratio_chart',name='silence_ratio_chart'),
    url(r'^lan_line_chart/$','kx.tongji.views.lan_line_chart',name='lan_line_chart'),
    url(r'^lan_stack_chart/$','kx.tongji.views.lan_stack_chart',name='lan_stack_chart'),
    url(r'^reg_tongji/$','kx.tongji.views.reg_tongji',name='reg_tongji'),
    url(r'^reg_chart/$','kx.tongji.views.reg_chart',name='reg_chart'),
)

