#_*_coding:utf-8_*_
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.conf import settings
from datetime import datetime
from apps.kx.models import KxUser


# 群
class Groups(models.Model):
    id = models.AutoField(primary_key=True)  # 高校群ID 10001~19999 普通群 >=20000
    name = models.CharField(max_length=30,verbose_name=_(u'群名称'))
    owner_id = models.OneToOneField(KxUser,verbose_name=_(u'群所有者Email'),related_name='owner_in')
    user_num = models.IntegerField(default=0,verbose_name=_(u'群用户人数'),editable=False)
    max_num = models.IntegerField(verbose_name=_(u'群最大用户数'))
    g_type = models.IntegerField(verbose_name=_(u'群类型'),default=1,help_text=_(u'1=普通群，2=高校群'))  # 1=普通群 2=高校群
    create_time = models.DateTimeField(default=datetime.now,verbose_name=_(u'创建时间'))
    creater_id = models.OneToOneField(KxUser,verbose_name=_(u'创建群的人'),editable=False,related_name='create_id')# 谁被加进来的

    class Meta:
        db_table = 'groups'
        verbose_name_plural = verbose_name = _(u'群')
    def __unicode__(self):
        return self.name


# 群用户
class GroupUser(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.IntegerField(verbose_name=_(u'群ID'))
    user_id = models.CharField(max_length=32,verbose_name=_(u'群用户Email')) # 谁被加进来的
    user_remark = models.CharField(max_length=20,null=True,blank=True,verbose_name=_(u'用户备注名'))  # 用户备注名
    share_print = models.BooleanField(verbose_name=_(u'是否可以共享打印机到群'),help_text=_(u'0:不能添加共享打印机到群'))  # 是否可以共享打印机到群 0=否
    join_time = models.DateTimeField(default=datetime.now,verbose_name=_(u'加入群的时间'))
    joiner_id = models.CharField(null=True,max_length=32) # 谁被加进来的

    class Meta:
        db_table = "group_user"
        verbose_name_plural = verbose_name = _(u'群用户')
    #def __unicode__(self):
    #    return self.user_id_id


# 申请加群记录
class GroupUserVerify(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.IntegerField(verbose_name=_(u'群ID'))
    user_id = models.IntegerField(verbose_name=_(u'申请用户ID'))  # 申请用户ID
    msg = models.CharField(max_length=50,verbose_name=_(u'申请用户留言'))  # 申请用户的留言
    create_time = models.DateTimeField()

    class Meta:
        db_table = "group_user_verify"
        verbose_name_plural = verbose_name = _(u'申请加群记录')


# 群用户打印权限
class GroupPrintAuth(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.IntegerField(verbose_name=_(u'群ID'))
    print_user_id = models.CharField(max_length=32,verbose_name=_(u'共享打印机的用户ID'))  # 共享打印机的用户ID
    user_id = models.CharField(max_length=32,verbose_name=_(u'使用这用户ID'))  # 使用者用户ID
    status = models.IntegerField(verbose_name=_(u'审核状态'),help_text=_(u'0=审核中，1=审核通过，2=拒绝'))  # 审核状态 0=审核中，1=审核通过，2=拒绝
    answer = models.CharField(null=True,max_length=30,verbose_name=_(u'提问回答'))
    create_time = models.DateTimeField(default=datetime.now,verbose_name=_(u'创建时间'))
    auth_time = models.DateTimeField(null=True) # 审核时间

    class Meta:
        db_table = "group_print_auth"
        verbose_name_plural = verbose_name = _(u'群用户打印权限')


# 打印机
class UserPrinter(models.Model):
    id = models.AutoField(primary_key=True)
    print_user_id = models.CharField(max_length=32,verbose_name=_(u'打印机用户ID'))
    print_name = models.CharField(max_length=30,verbose_name=_(u'打印机名称'))  # 打印机名称
    print_code = models.CharField(max_length=260,verbose_name=_(u'打印机序列号'))  # 打印机序列号
    remark = models.CharField(null=True,max_length=100) #打印机备注
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_printer"

# 群打印机
class GroupPrint(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.IntegerField()
    printer_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "group_print"
        verbose_name_plural = verbose_name = _(u'群打印机')


# 群管理员
class GroupManager(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.IntegerField(verbose_name=_(u'群ID'))
    user_id = models.CharField(max_length=32,verbose_name=_(u'管理员Email'))

    class Meta:
        db_table = "group_manager"
        verbose_name_plural = verbose_name = _(u'群管理员')
