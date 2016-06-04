from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'shareFile/', include('sharefile.urls')),
    #url(r'client/', include('client.urls')),
    url(r'onlineUser/', include('online_user.urls')),
    url(r'^$','kx.views.index',name='index'),

    # url(r'^qm_web/', include('qm_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-token-auth/','auth.views.obtain_auth_token'), 
    url(r'^api-register/','auth.views.api_register'), 
)
urlpatterns += patterns('',
    url(r'^MsgBoard/',include("kx.msg_board.urls")),
    url(r'^SoftRecord/',include("kx.api.urls",)),
    url(r'^User/',include("kx.accounts.urls")),
    url(r'^Blog/',include("kx.blog.urls")),
    url(r'^BugReport/',include("kx.bug_report.urls")),
    url(r'^Pub/',include("kx.publish.urls")),
)

if settings.DEBUG:
    #urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT ) 
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT ) 
