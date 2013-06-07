from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.online_user.views.onlineFriends', name='onlineFriends'),
)
