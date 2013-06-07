from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.sharefile.views.friendFiles', name='friendFiles'),
    url(r'sendMsg2cscServer/$', 'apps.sharefile.views.sendMyInfoToServer', name='sendMsg2cscServer'),
    url(r'^peerPort/$', 'apps.sharefile.views.peerPort', name='peerPort'),
)
