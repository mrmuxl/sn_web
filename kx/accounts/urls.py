#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^accounts/register/$','kx.views.register',name='register'),
    url(r'^accounts/login/$','kx.views.login',name='login'),
    url(r'^accounts/logout/$','kx.views.logout',name='logout'),
    url(r'^accounts/info/$','kx.views.info',name='info'),
    url(r'^accounts/avatar/$','kx.views.avatar',name='avatar'),
    url(r'^accounts/chpasswd/$','kx.views.chpasswd',name='passwd'),
    url(r'^accounts/check/$','kx.views.check',name='check'),
    url(r'^accounts/save/$','kx.views.save',name='save'),
    
    url(r'^accounts/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^accounts/reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    #url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    #url(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
)
