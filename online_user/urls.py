from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'online_user.views.onlineFriends', name='onlineFriends'),
)
