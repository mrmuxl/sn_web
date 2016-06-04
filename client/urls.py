from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
	(r'^login/$', TemplateView.as_view(template_name="client_login.html")),
    (r'^friend/feed/$', TemplateView.as_view(template_name="feed.html")),
    (r'^friend/addfriends/$', TemplateView.as_view(template_name="addfriends.html")),
    (r'^file/index/$', TemplateView.as_view(template_name="file_index.html")),
    (r'^trans/processing/$', TemplateView.as_view(template_name="trans_processing.html")),
    (r'^print/index/$', TemplateView.as_view(template_name="print_index.html")),
    (r'^help/nav/$', TemplateView.as_view(template_name="help_nav.html")),
    (r'^help/index/$', TemplateView.as_view(template_name="help_index.html")),
    (r'^help/addfriends/$', TemplateView.as_view(template_name="help_addfriend.html")),
    (r'^help/chat/$', TemplateView.as_view(template_name="help_chat.html")),
    (r'^help/fileshare/$', TemplateView.as_view(template_name="help_fileshare.html")),
    (r'^help/fileshare/auth/$', TemplateView.as_view(template_name="help_fileshare_auth.html")),
    (r'^help/fileshare/friend/$', TemplateView.as_view(template_name="help_fileshare_friend.html")),
    (r'^help/trans/$', TemplateView.as_view(template_name="help_trans.html")),
    (r'^help/trans/upload/$', TemplateView.as_view(template_name="help_trans_upload.html")),
    (r'^help/print/$', TemplateView.as_view(template_name="help_print.html")),
)