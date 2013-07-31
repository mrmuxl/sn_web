#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from apps.kx.models import KxUser
from datetime import datetime

class ProductInfo(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=200,verbose_name = _(u'产品名称'))
    desc = models.TextField(verbose_name = _(u'产品描述'))
    price = models.IntegerField(verbose_name = _(u'单价'))
    stocked = models.IntegerField(verbose_name = _(u'库存'))
    class Meta:
        db_table = 'product_info'
        verbose_name_plural = verbose_name = _(u'产品信息')
    def __unicode__(self):
        return self.name

class OrderInfo(models.Model):
    id = models.AutoField(primary_key = True)
    order_id = models.CharField(db_index=True,unique=True,max_length=20,verbose_name=_(u'订单ID')) 
    create_at = models.DateTimeField(default = datetime.now(),verbose_name = _(u'创建时间'))
    buy_user = models.EmailField(_(u'购买人'),max_length=50)
    buy_product = models.ForeignKey(ProductInfo,verbose_name = _(u'购买产品'))
    number = models.IntegerField(verbose_name=_(u'购买数量'))
    total_fee = models.IntegerField(verbose_name=_(u'支付总额'))
    pay_status = models.BooleanField(verbose_name=_(u'支付状态'),help_text=_(u'0：未付款，1：已付款'))
    pay_at = models.DateTimeField(default = datetime(1970,1,1),verbose_name = _(u'付款时间'))
    trade_no = models.CharField(default ='0',db_index=True,max_length=64,verbose_name=_(u'支付宝交易号')) 
    class Meta:
        db_table = 'order_info'
        verbose_name_plural = verbose_name = _(u'订单信息')
    def __unicode__(self):
        return self.order_id
