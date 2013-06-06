#_*_coding:utf-8_*_

from django.db import models

class KxSoftAd(models.Model):
    id          = models.IntegerField(primary_key = True)
    title       = models.CharField(max_length = 50L,verbose_name=u'标题')
    ad_url      = models.CharField(max_length = 200L,verbose_name=u'推广链接')
    exp_day     = models.DateField(verbose_name=u'过期时间')
    creater_id  = models.CharField(max_length=32L)
    create_time = models.DateTimeField()
    class Meta:
        db_table = 'kx_soft_ad'
        verbose_name_plural = verbose_name = u'推广'
