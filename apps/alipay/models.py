#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from apps.kx.models import KxUser
from datetime import datetime

class ProductInfo(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=600)
    price = models.IntegerField()
    stocked = models.IntegerField()
    class Meta:
        db_table = 'product'
        verbose_name_plural = verbose_name = _(u'产品信息')

class OrderInfo(models.Model):
    id = models.AutoField(primary_key = True)
    order_id = models.CharField(db_index=True,unique=True,max_length=24,verbose_name=_(u'订单ID')) 
    create_at = models.DateTimeField(default = datetime.now(),verbose_name = _(u'订单创建时间'))
    buy_user = models.EmailField(_(u'购买人'),max_length=50)
    buy_product = models.ForeignKey(ProductInfo)
    number = models.IntegerField(verbose_name=_(u'购买数量'))
    pay_status = models.BooleanField(verbose_name=_(u'支付状态'),help_text=_(u'0：未付款，1：已付款'))
    pay_at = models.DateTimeField(default = datetime.now(),verbose_name = _(u'付款时间'))
    class Meta:
        db_table = 'order'
        verbose_name_plural = verbose_name = _(u'订单信息')
