#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from apps.kx.models import KxUser
from datetime import datetime

class OperatorCategory(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=255, unique=True, verbose_name=_(u'分类名称'))
    ordering = models.IntegerField(blank=True, null=True, verbose_name=_(u'排序序'))
    class Meta:
        db_table = 'operator_category'
        verbose_name_plural = verbose_name = _(u'运营商分类')
        ordering = ['ordering',]
    def __unicode__(self):
        return self.name

class Operator(models.Model):
    id = models.AutoField(primary_key = True)
    category = models.ForeignKey(OperatorCategory, verbose_name=_(u'分类'))
    user = models.OneToOneField(KxUser,verbose_name = _(u'邮箱'))
    name = models.CharField(max_length=255, verbose_name=_(u'运营商名称'))
    printer_num = models.IntegerField(default=0,verbose_name=_(u'运营商可以使用的打印机数'))
    used_num = models.IntegerField(default=0,verbose_name=_(u'已经使用的打印机数'))
    qq = models.CharField(default='0',max_length=14, verbose_name=_(u'运营商名称'))
    tel = models.CharField(default='0',max_length=14,verbose_name=_(u'电话号码'))
    company_tel= models.CharField(default='0',max_length=14,verbose_name=_(u'公司电话'))
    school  = models.CharField(max_length=260,verbose_name=_(u'学校名称'))
    resource =  models.TextField(verbose_name=_(u'资源和优势'))
    created = models.DateTimeField(default=datetime.now(), verbose_name=_('创建时间'))
    modified = models.DateTimeField(default=datetime.now(), verbose_name=_('修改时间'))
    expire = models.DateTimeField(default=datetime(1970,1,1), verbose_name=_(u'过期时间'))
    status = models.IntegerField(verbose_name=_(u'运营商状态'),default=False)
    class Meta:
        db_table = 'operator'
        verbose_name_plural = verbose_name = _(u'运营商')
    def __unicode__(self):
        return self.name

class OperatorAssistant(models.Model):
    id = models.AutoField(primary_key = True)
    operator = models.ForeignKey(Operator,verbose_name = _(u'运营商'))
    user = models.OneToOneField(KxUser,verbose_name = _(u'运营专员邮箱'))
    name = models.CharField(max_length=255, unique=True, verbose_name=_(u'运营专员名称'))
    created = models.DateTimeField(default=datetime.now(), verbose_name=_('创建时间'))
    status = models.IntegerField(verbose_name=_(u'运营专员状态'),default=False)
    class Meta:
        db_table = 'operator_assistant'
        verbose_name_plural = verbose_name = _(u'运营专员')
    def __unicode__(self):
        return self.name
