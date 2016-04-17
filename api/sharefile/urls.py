from django.conf.urls import patterns, include, url
from api.sharefile import views

urlpatterns = patterns('',
    url(r'^$', 'api.sharefile.views.friendFiles', name='friendFiles'),
)
