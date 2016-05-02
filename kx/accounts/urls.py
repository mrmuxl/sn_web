#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','kx.accounts.views.login',name='login'),
    url(r'^register/?$','kx.accounts.views.register',name='register'),
    url(r'^register/invate_code/(.+)$','kx.accounts.views.register',name='invate_code'),
    url(r'^login/?$','kx.accounts.views.login',name='login'),
    url(r'^logout/?$','kx.accounts.views.logout',name='logout'),
    url(r'^info/?$','kx.accounts.views.info',name='info'),
    url(r'^avatar/?$','kx.accounts.views.avatar',name='avatar'),
    url(r'^changePWD/?$','kx.accounts.views.chpasswd',name='chpasswd'),
    url(r'^check/?$','kx.accounts.views.check',name='check'),
    url(r'^save/?$','kx.accounts.views.save',name='save'),
    url(r'^findPwd/?$','kx.accounts.views.findPwd',name='findPwd'),
    url(r'^protocol/?$','kx.accounts.views.protocol',name='protocol'),
    url(r'^to_active/?$','kx.accounts.views.to_active',name='to_active'),
    url(r'^account_verify/?$','kx.accounts.views.account_verify',name='account_verify'),
    url(r'^activate/verify/(.+)$','kx.accounts.views.activate',name='activate'),
    url(r'^verify_success/$','kx.accounts.views.verify_success',name='verify_success'),
    url(r'^cadd/?$','kx.api.views.cadd',name='cadd'),
    url(r'^invate/$','kx.api.views.invate',name='invate'),
    
    #url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    #url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    #url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    #url(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
)
