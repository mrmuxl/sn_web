from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'sharefile.views.friendFiles', name='friendFiles'),
    url(r'^peerPort/(?P<mac>.*)$', 'sharefile.views.peerPort', name='peerPort'),
)
