#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = patterns('',
    #url(r'^order_info/?$', login_required(TemplateView.as_view(template_name = 'alipay/order_info.html')), name="order_info"),
    url(r'^order_info/?$','apps.alipay.views.order_info',name="order_info"),
    url(r'^order_result/?$','apps.alipay.views.create_order',name="create_order"),
    #url(r'^successful/?$','apps.alipay.views.successful', name="alipay_successful"),
    url(r'^error/?$', TemplateView.as_view(template_name = 'alipay/error.html'), name="alipay_error"),
    url(r'^return_url/?$','apps.alipay.views.return_url_handler',name='alipay_return_url'),
    url(r'^notify_url/?$','apps.alipay.views.notify_url_handler',name='alipay_notify_url'),
)
