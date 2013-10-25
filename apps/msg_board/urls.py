#_*_coding:utf-8_*_
from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView

#urlpatterns = patterns('',
#    url(r'^$','apps.msg_board.views.msg_board',name ='msg_index'),
#    url(r'^msg_index/?$','apps.msg_board.views.msg_board',name ='msg_index'),
#    url(r'^add_msg/?$','apps.msg_board.views.add_msg',name ='add_msg'),
#    url(r'^del_msg/?$','apps.msg_board.views.del_msg',name ='del_msg'),
#    url(r'^check_msg/?$','apps.msg_board.views.check_msg',name ='check_msg'),
#)


urlpatterns = patterns('',
    url(r'^msg_index/?$',RedirectView.as_view(url='index'),name ='msg_index'),
    url(r'^$','apps.forum.views.index',name ='forum_index'),
    url(r'^index/?$','apps.forum.views.index',name ='forum_index'),
    url(r'^add/?$','apps.forum.views.add',name ='forum_add'),
    url(r'^post/(?P<pid>\d+)/?$', 'apps.forum.views.post',name='forum_post'),
    url(r'^reply/?$','apps.forum.views.reply',name ='forum_reply'),
    url(r'^vote/?$','apps.forum.views.vote',name ='forum_vote'),
    url(r'^check_msg/?$','apps.msg_board.views.check_msg',name ='check_msg'),
)

