#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import datetime
from datetime import date
from django.conf import settings


def get_image_path(instance,filename):
    date_str =date.strftime(date.today(),"%Y/%m/%d")
    return '/'.join(["spool_image",date_str,instance.uuid])+'.jpg'

class Spool(models.Model):
    id            = models.AutoField(primary_key = True)
    uuid          = models.CharField(max_length = 50, unique = True)
    origin_email  = models.EmailField(verbose_name=u'发起人邮件地址', max_length=50)
    accept_email  = models.EmailField(verbose_name=u'接受人邮件地址', max_length=50)
    printer_name  = models.CharField(max_length = 255, blank = True)
    file_name      = models.CharField(max_length = 255, blank = True)
    page_num      = models.IntegerField()
    print_time    = models.DateTimeField(default=datetime.now(),verbose_name=_(u'打印时间'))
    thumb         = models.ImageField(upload_to=get_image_path)
    status        = models.BooleanField(verbose_name=_(u'是否显示'))
    class Meta:
        db_table = 'print_spool'
        verbose_name_plural = verbose_name = _(u'打印队列')
    def __unicode__(self):
        return self.file_name
        
