#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','apps.accounts.views.login',name='login'),
    url(r'^register/?$','kx.accounts.views.register',name='register'),
    url(r'^register/invate_code/(.+)$','apps.accounts.views.register',name='invate_code'),
    url(r'^login/?$','apps.accounts.views.login',name='login'),
    url(r'^logout/?$','apps.accounts.views.logout',name='logout'),
    url(r'^info/?$','apps.accounts.views.info',name='info'),
    url(r'^check/?$','apps.accounts.views.check',name='check'),
    url(r'^save/?$','apps.accounts.views.save',name='save'),
    
    #url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    #url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    #url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    #url(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
)
urlpatterns += patterns('',
    url(r'^protocol/?$','apps.accounts.views.protocol',name='protocol'),
    url(r'^cadd/?$','apps.api.views.cadd',name='cadd'),
    url(r'^avatar/?$','apps.accounts.views.avatar',name='avatar'),

)
urlpatterns += patterns('',
    url(r'^verify_success/$','apps.accounts.views.verify_success',name='verify_success'),
    url(r'^account_verify/?$','apps.accounts.views.account_verify',name='account_verify'),
    url(r'^activate/verify/(.+)$','apps.accounts.views.activate',name='activate'),
    url(r'^invate/$','apps.api.views.invate',name='invate'),
    url(r'^to_active/?$','apps.accounts.views.to_active',name='to_active'),
    url(r'^invite_msg/(\w+)/?$','apps.accounts.views.invite_msg',name='invite_msg'),
)

urlpatterns += patterns('',
    url(r'^findPwd/?$','apps.accounts.views.findPwd',name='findPwd'),
    url(r'^resetPwd/verify/(.+)$','apps.accounts.views.resetPwd',name='resetPwd'),
    url(r'^rePwd/?$','apps.accounts.views.rePwd',name='rePwd'),
    url(r'^changePWD/?$','apps.accounts.views.chpasswd',name='chpasswd'),
)
