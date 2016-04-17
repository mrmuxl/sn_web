from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^sharefile/',include('api.sharefile.urls')),
)
