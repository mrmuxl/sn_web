from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','kx.views.index',name='index'),
    url(r'^msg_board/$','kx.views.msg_board',name='msg_show'),
    url(r'^msg_board/add_msg/$','kx.views.add_msg',name='add_msg'),

    # url(r'^qm_web/', include('qm_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api-token-auth/','api.auth.views.obtain_auth_token'), 
)
urlpatterns += patterns('',
    url(r'^SoftRecord/',include("kx.api.urls",)),
    url(r'^accounts/',include("kx.accounts.urls")),
    url(r'^blog/',include("kx.blog.urls")),
)

if settings.DEBUG:
    #urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT ) 
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT ) 
