#_*_coding:utf-8_*_

from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

class KxSoftAd(models.Model):
    id          = models.AutoField(primary_key = True)
    title       = models.CharField(max_length = 50L,verbose_name=u'标题')
    ad_url      = models.URLField(max_length = 200L,verbose_name=u'推广链接')
    exp_day     = models.DateField(verbose_name=u'过期时间')
    creater_id  = models.CharField(max_length=32L)
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

