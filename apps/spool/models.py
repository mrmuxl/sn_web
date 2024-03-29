#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import datetime,date
from django.conf import settings


#def get_image_path(instance,filename):
#    date_str =date.strftime(date.today(),"%Y/%m/%d")
#    return '/'.join(["spool_image",date_str,instance.uuid])+'.jpg'

class Spool(models.Model):
    id            = models.AutoField(primary_key = True)
    uuid          = models.CharField(max_length = 50, unique = True,verbose_name=_(u'唯一码'))
    origin_email  = models.EmailField(verbose_name=_(u'发起人邮件地址'), max_length = 50)
    origin_uuid   = models.CharField(verbose_name=_(u'发起人的机器码'), max_length = 260)
    accept_email  = models.EmailField(verbose_name=_(u'接受人邮件地址'), max_length = 50)
    accept_uuid   = models.CharField(verbose_name=_(u'接受人的机器码'), max_length = 260)
    printer_name  = models.CharField(verbose_name=_(u'打印机名称'), max_length = 260, blank = True)
    printer_uuid  = models.CharField(verbose_name=_(u'打印机唯一码'),max_length = 260, blank = True)
    file_name     = models.CharField(verbose_name=_(u'打印文件名'),max_length = 260, blank = True)
    file_path     = models.CharField(verbose_name=_(u'接受方打印文件路径'), blank = True,max_length=260)
    file_client_path  = models.CharField(verbose_name=_(u'发起方打印文件路径'), blank = True,max_length=260)
    page_num      = models.IntegerField(default = 0,verbose_name=_(u'文件打印张数'))
    print_time    = models.DateTimeField(default=datetime.now, verbose_name=_(u'打印时间'))
    status        = models.IntegerField(default=1,verbose_name=_(u'打印队列状态'),help_text=_(u'0=不输出，1=队列中，2=打印成功，3=打印失败，4=取消，5=删除，6=取消'))
    create_at     = models.DateTimeField(default=datetime.now, verbose_name=_(u'加入队列时间'))
    status_time   = models.DateTimeField(default=datetime.now, verbose_name=_(u'队列状态修改时间'))
    class Meta:
        db_table = 'print_spool'
        verbose_name_plural = verbose_name = _(u'打印队列')
    def __unicode__(self):
        return self.uuid
        
