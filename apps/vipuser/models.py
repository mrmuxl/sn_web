#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from apps.kx.models import KxUser
from datetime import datetime

class VIPUser(models.Model):
    email = models.OneToOneField(KxUser,to_field='email',db_column='email',related_name='vipuser_email',verbose_name = _(u'邮箱'))
    is_vip = models.BooleanField(verbose_name=_(u'是否vip用户'))
    create_at = models.DateTimeField(default = datetime.now(),verbose_name = _(u'创建时间'))
    expire = models.DateTimeField(default = datetime(1970,1,1),verbose_name = _(u'过期时间'))
    class Meta:
        db_table = 'vipuser'
        verbose_name_plural = verbose_name = _(u'VIP用户')
    def __unicode__(self):
        return self.email_id

class Print(models.Model):
    email = models.OneToOneField(KxUser,to_field='email',db_column='email',related_name='print',verbose_name = _(u'邮箱'))
    is_print = models.BooleanField(verbose_name=_(u'是否打印共享用户'),default=False)
    print_num = models.IntegerField(verbose_name=_(u'打印共享授权人数'),default =0)
    used_print_num = models.IntegerField(verbose_name=_(u'打印共享已经授权人数'),default =0)
    create_at = models.DateTimeField(default = datetime.now(),verbose_name = _(u'创建时间'))
    expire = models.DateTimeField(default = datetime(1970,1,1),verbose_name = _(u'过期时间'))
    class Meta:
        db_table = 'print'
        verbose_name_plural = verbose_name = _(u'打印共享')
    def __unicode__(self):
        return self.email_id

class Shared(models.Model):
    email = models.OneToOneField(KxUser,to_field='email',db_column='email',related_name='shared',verbose_name = _(u'邮箱'))
    is_shared = models.BooleanField(verbose_name=_(u'是否文件共享用户'),default=False)
    shared_num = models.IntegerField(verbose_name=_(u'文件共享授权人数'),default =0)
    used_shared_num = models.IntegerField(verbose_name=_(u'文件共享已经授权人数'),default =0)
    create_at = models.DateTimeField(default = datetime.now(),verbose_name = _(u'创建时间'))
    expire = models.DateTimeField(default = datetime(1970,1,1),verbose_name = _(u'过期时间'))
    class Meta:
        db_table = 'shared'
        verbose_name_plural = verbose_name = _(u'文件共享')
    def __unicode__(self):
        return self.email_id

class PrintAccess(models.Model):
    email = models.ForeignKey(Print,to_field='email',db_column='email',related_name='print_access',verbose_name = _(u'邮箱'))
    access_user = models.ForeignKey(KxUser,to_field='email',db_column='access_user',related_name='print_access_user',verbose_name = _(u'Print被授权用户邮箱'))
    create_at = models.DateTimeField(default = datetime.now(),verbose_name = _(u'创建时间'))
    status = models.BooleanField(verbose_name=_(u'是/否有效共享用户'),default=False)
    class Meta:
        db_table = 'print_access'
        verbose_name_plural = verbose_name = _(u'打印共享授权')
    def __unicode__(self):
        return self.email_id

class SharedAccess(models.Model):
    email = models.ForeignKey(Shared,to_field='email',db_column='email',related_name='shared_access',verbose_name = _(u'邮箱'))
    access_user = models.ForeignKey(KxUser,to_field='email',db_column='access_user',related_name='shared_access_user',verbose_name = _(u'Shared被授权用户邮箱'))
    create_at = models.DateTimeField(default = datetime.now(),verbose_name = _(u'创建时间'))
    status = models.BooleanField(verbose_name=_(u'是/否有效共享用户'),default=False)
    class Meta:
        db_table = 'shared_access'
        verbose_name_plural = verbose_name = _(u'文件共享授权')
    def __unicode__(self):
        return self.email_id



