from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'kx.views.index', name='index'),
    url(r'^msg_board/','kx.views.msg_board'),
    url(r'^msg_board/add_msg/','kx.views.add_msg'),
    url(r'^user/register/','kx.views.register',name='register'),
    url(r'^user/login/','kx.views.login',name='login'),
    url(r'^user/logout/','kx.views.login',name='logout'),
    url(r'^user/info/','kx.views.login',name='info'),
    url(r'^user/check/','kx.views.check',name='check'),
    url(r'^user/save/','kx.views.save',name='save'),



    # url(r'^qm_web/', include('qm_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
