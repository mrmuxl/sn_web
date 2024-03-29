#_*_coding:utf-8_*_

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','apps.kx.views.index',name='index'),
    #url(r'^buy/?$','apps.kx.views.buy',name='buy'),
    url(r'^buy/?$',RedirectView.as_view(url='alipay/order_info?c=1'),name ='buy'),
    url(r'^printer/?$','apps.ad.views.printer',name='printer'),
    url(r'^fzu/?$','apps.ad.views.fzu',name='fzu'),
    url(r'^jxxy/?$','apps.ad.views.jxxy',name='ad_jxxy'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
    url(r'shareFile/', include('apps.sharefile.urls')),
    url(r'client/', include('apps.client.urls')),
    url(r'onlineUser/', include('apps.online_user.urls')),
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
    url(r'^spool/',include("apps.spool.urls")),
    url(r'^group/',include("apps.group.urls")),
    url(r'^account/',include("apps.accounts.urls_account")),
    #url(r'^user/',include("apps.user.urls")),
)

if settings.DEBUG:
    urlpatterns += patterns('', url(r'^forums/',include("apps.forum.urls")),)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT ) 
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT ) 
