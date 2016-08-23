#_*_coding:utf-8_*_

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'shareFile/', include('apps.sharefile.urls')),
    url(r'client/', include('apps.client.urls')),
    url(r'onlineUser/', include('apps.online_user.urls')),
    url(r'^$','apps.kx.views.index',name='index'),

    # url(r'^qm_web/', include('qm_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #这个连接在发布时要去掉
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/','apps.auth.views.obtain_auth_token'), 
    url(r'^api-register/','apps.auth.views.api_register'), 
)
urlpatterns += patterns('',
    url(r'^MsgBoard/',include("apps.msg_board.urls")),
    url(r'^SoftRecord/',include("apps.kx.api.urls",)),
    url(r'^User/',include("apps.accounts.urls")),
    url(r'^Blog/',include("apps.blog.urls")),
    url(r'^BugReport/',include("apps.bug_report.urls")),
    url(r'^Pub/',include("apps.publish.urls")),
    url(r'^SoftAd/',include("apps.ad.urls")),
    url(r'^vipuser/',include("apps.vipuser.urls")),
    url(r'^alipay/',include("apps.alipay.urls")),
)

if settings.DEBUG:
    #urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT ) 
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT ) 
