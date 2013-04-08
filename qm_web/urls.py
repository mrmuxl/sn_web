from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'kx.views.index', name='index'),
    url(r'^msg_board/$','kx.views.msg_board',name='msg_show'),
    url(r'^msg_board/add_msg/$','kx.views.add_msg'),
    url(r'^blog/$','kx.views.post',name='show'),
    url(r'^SoftRecord/tongji/$','kx.views.tongji',name='tongji'),
    url(r'^SoftRecord/login_tongji/$','kx.views.login_tongji',name='login_tongji'),
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



    # url(r'^qm_web/', include('qm_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    url(r'^api-token-auth/','api.auth.views.obtain_auth_token'), 
)

if settings.DEBUG:
    #urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT ) 
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT ) 
