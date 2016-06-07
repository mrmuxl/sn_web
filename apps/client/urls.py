from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from apps.client.decorators import sn_required, snlogin_required

urlpatterns = patterns('',
	(r'^login/$', 'apps.client.views.login'),
    (r'^silenceLogin/$', 'apps.client.views.silencelogin'),
    (r'^friend/feed/$', snlogin_required(TemplateView.as_view(template_name="feed.html"))),
    (r'^friend/addfriends/$', snlogin_required(TemplateView.as_view(template_name="addfriends.html"))),
    (r'^file/index/$', snlogin_required(TemplateView.as_view(template_name="file_index.html"))),
    (r'^trans/processing/$', snlogin_required(TemplateView.as_view(template_name="trans_processing.html"))),
    (r'^print/index/$', snlogin_required(TemplateView.as_view(template_name="print_index.html"))),
    (r'^help/nav/$', sn_required(TemplateView.as_view(template_name="help_nav.html"))),
    (r'^help/index/$', snlogin_required(TemplateView.as_view(template_name="help_index.html"))),
    (r'^help/addfriends/$', snlogin_required(TemplateView.as_view(template_name="help_addfriend.html"))),
    (r'^help/chat/$', snlogin_required(TemplateView.as_view(template_name="help_chat.html"))),
    (r'^help/fileshare/$', snlogin_required(TemplateView.as_view(template_name="help_fileshare.html"))),
    (r'^help/fileshare/auth/$', snlogin_required(TemplateView.as_view(template_name="help_fileshare_auth.html"))),
    (r'^help/fileshare/friend/$', snlogin_required(TemplateView.as_view(template_name="help_fileshare_friend.html"))),
    (r'^help/trans/$', snlogin_required(TemplateView.as_view(template_name="help_trans.html"))),
    (r'^help/trans/upload/$', snlogin_required(TemplateView.as_view(template_name="help_trans_upload.html"))),
    (r'^help/print/$', snlogin_required(TemplateView.as_view(template_name="help_print.html"))),
    (r'^csrf/$', snlogin_required(TemplateView.as_view(template_name="csrf.html"))),
)
