#_*_coding:utf-8_*_

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    #url(r'^$','apps.alipay.views.index',name='alipay_index'),
    url(r'order_result/$','apps.alipay.views.order_result',name="order_result"),
    url(r'^$', TemplateView.as_view(template_name = 'alipay/plans.html'),name="alipay_plans"),
    url(r'^success/$', TemplateView.as_view(template_name = 'alipay/success.html'), name="alipay_success"),
    url(r'^error/$', TemplateView.as_view(template_name = 'alipay/error.html'), name="alipay_error"),
    url(r'return_url$','apps.alipay.views.return_url_handler',name='alipay_return_url'),
    url(r'notify_url$','apps.alipay.views.notify_url_handler',name='alipay_notify_url'),
)
