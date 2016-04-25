#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','kx.msg_board.views.msg_board',name ='msg_index'),
    url(r'^msg_index/?$','kx.msg_board.views.msg_board',name ='msg_index'),
    url(r'^add_msg/?$','kx.msg_board.views.add_msg',name ='add_msg'),
    url(r'^del_msg/?$','kx.msg_board.views.del_msg',name ='del_msg'),
)

