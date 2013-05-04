from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'sharefile.views.friendFiles', name='friendFiles'),
    url(r'sendMsg2cscServer/$', 'sharefile.views.sendMyInfoToServer', name='sendMsg2cscServer'),
    url(r'^peerPort/$', 'sharefile.views.peerPort', name='peerPort'),
)
