from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from apps.client.decorators import sn_required, snlogin_required

urlpatterns = patterns('',
    (r'^friendList/$', 'apps.client.v_friend.friendList'),
)
