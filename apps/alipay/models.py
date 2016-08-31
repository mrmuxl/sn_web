#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from apps.kx.models import KxUser
from datetime import datetime

PRODUCT_CHOICES = (
    (1,u'VIP'),
    (2,u'打印共享'),
    (3,u'打印共享用户授权'),
    (4,u'文件共享'),
    (5,u'文件共享用户授权'),
)

class ProductInfo(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=200,verbose_name = _(u'产品名称'))
    slug = models.CharField(max_length=50,blank=True,verbose_name = _(u'标签'))
    category = models.IntegerField(verbose_name = _(u'产品分类'),default = 0,choices=PRODUCT_CHOICES,help_text=_(u'产品分类，从 1 开始， 0 代表无类别，1：VIP,2：打印共享，3：打印共享文件授权，4：文件共享，5：文件共享用户授权)'))
    desc = models.TextField(verbose_name = _(u'产品描述'))
    price = models.DecimalField(verbose_name = _(u'单价'),max_digits=10,decimal_places=2,default=0.00)
    stocked = models.IntegerField(verbose_name = _(u'库存'))
    order_num = models.IntegerField(verbose_name = _(u'排序'),default = 0)
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
    total_fee = models.DecimalField(verbose_name=_(u'支付总额'),max_digits=10,decimal_places=2,default=0.00)
    pay_status = models.BooleanField(verbose_name=_(u'支付状态'),help_text=_(u'0：未付款，1：已付款'))
    pay_at = models.DateTimeField(default = datetime(1970,1,1),verbose_name = _(u'付款时间'))
    trade_no = models.CharField(default ='0000',db_index=True,max_length=64,verbose_name=_(u'支付宝交易号')) 
    class Meta:
        db_table = 'order_info'
        verbose_name_plural = verbose_name = _(u'订单信息')
    def __unicode__(self):
        return self.order_id
