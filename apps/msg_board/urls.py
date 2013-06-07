#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','apps.msg_board.views.msg_board',name ='msg_index'),
    url(r'^msg_index/?$','apps.msg_board.views.msg_board',name ='msg_index'),
    url(r'^add_msg/?$','apps.msg_board.views.add_msg',name ='add_msg'),
    url(r'^del_msg/?$','apps.msg_board.views.del_msg',name ='del_msg'),
    url(r'^check_msg/?$','apps.msg_board.views.check_msg',name ='check_msg'),
)

