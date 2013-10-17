#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from apps.kx.models import KxUser
from datetime import datetime

class KxSoftAd(models.Model):
    id          = models.AutoField(primary_key = True)
    title       = models.CharField(max_length = 50L,verbose_name=u'标题')
    ad_url      = models.URLField(max_length = 200L,verbose_name=u'推广链接')
    exp_day     = models.DateField(verbose_name=u'过期时间')
    creater_id  = models.CharField(default=datetime.now,max_length=32L)
    create_time = models.DateTimeField(verbose_name =u'创建时间')
    class Meta:
        db_table = 'kx_soft_ad'
        verbose_name_plural = verbose_name = u'推广'


class PrinterPop(models.Model):
    id = models.AutoField(primary_key = True)
    email = models.EmailField(verbose_name=_(u'推广邮件地址'), max_length = 50)
    create_at = models.DateTimeField(default=datetime.now(), verbose_name=_(u'加入时间'))
    class Meta:
        db_table = 'print_pop'
        verbose_name_plural = verbose_name = u'创业'
    def __unicode__(self):
        return self.email

class FZu(models.Model):
    id = models.AutoField(primary_key = True)
    email = models.EmailField(verbose_name=_(u'推广邮件地址'), max_length = 50)
    create_at = models.DateTimeField(default=datetime.now(), verbose_name=_(u'加入时间'))
    class Meta:
        db_table = 'print_fzu'
        verbose_name_plural = verbose_name =_( u'福州大学')
    def __unicode__(self):
        return self.email


class OperatorCategory(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=255,verbose_name=_(u'分类名称'))
    cid = models.IntegerField(verbose_name=_(u'分类id'),help_text=_(u'1个人用户，2运营商，3企业主'))#识别角色用1是个人用户，2是运营商，3是企业主
    ordering = models.IntegerField(blank=True, null=True, verbose_name=_(u'排序序'))
    class Meta:
        db_table = 'operator_category'
        verbose_name_plural = verbose_name = _(u'运营商分类')
        ordering = ['ordering',]
    def __unicode__(self):
        return self.name

class Operator(models.Model):
    id = models.AutoField(primary_key = True)
    category = models.ForeignKey(OperatorCategory,default=1, verbose_name=_(u'分类'))
    user = models.OneToOneField(KxUser,verbose_name = _(u'邮箱'))
    name = models.CharField(max_length=255, verbose_name=_(u'运营商名称'))
    printer_num = models.IntegerField(default=0,verbose_name=_(u'运营商可以使用的打印机数'))
    used_num = models.IntegerField(default=0,verbose_name=_(u'已经使用的打印机数'))
    qq = models.CharField(default='0',max_length=14, verbose_name=_(u'QQ'))
    tel = models.CharField(default='0',max_length=14,verbose_name=_(u'电话号码'))
    school  = models.CharField(max_length=255,blank=True,null=True,verbose_name=_(u'学校名称'))
    resource =  models.TextField(verbose_name=_(u'资源和优势'))
    created = models.DateTimeField(default=datetime.now, verbose_name=_('创建时间'))
    modified = models.DateTimeField(default=datetime.now, verbose_name=_('修改时间'))
    expire = models.DateTimeField(default=datetime(1970,1,1), verbose_name=_(u'过期时间'))
    status = models.IntegerField(verbose_name=_(u'运营商状态'),default=0)
    class Meta:
        db_table = 'operator'
        verbose_name_plural = verbose_name = _(u'运营商')
    def __unicode__(self):
        return self.name

class OperatorAssistant(models.Model):
    id = models.AutoField(primary_key = True)
    operator = models.ForeignKey(Operator,verbose_name = _(u'运营商'))
    user = models.OneToOneField(KxUser,verbose_name = _(u'运营专员邮箱'))
    #name = models.CharField(max_length=255,verbose_name=_(u'运营专员名称'))
    created = models.DateTimeField(default=datetime.now, verbose_name=_('创建时间'))
    status = models.IntegerField(verbose_name=_(u'运营专员状态'),default=0)
    class Meta:
        db_table = 'operator_assistant'
        verbose_name_plural = verbose_name = _(u'运营专员')
    def __unicode__(self):
        #return self.operator.user.email
        return self.user.email
