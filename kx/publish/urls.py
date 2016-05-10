#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','kx.publish.views.publish_index',name ='publish_index'),
    url(r'add/?$','kx.publish.views.publish_add',name ='publish_add'),
    url(r'edit/?$','kx.publish.views.publish_add',name ='publish_edit'),
    url(r'do_pub/?$','kx.publish.views.do_pub',name ='do_pub'),
    url(r'del_pub/?$','kx.publish.views.del_pub',name ='del_pub'),
)

