#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import datetime
from apps.kx.models import KxUser

class KxPub(models.Model):
    id           = models.AutoField(primary_key = True)
    ver          = models.CharField(max_length = 30, unique = True)
    pub_desc     = models.CharField(max_length = 600)
    install_file = models.CharField(max_length = 100, blank = True)
    install_md5  = models.CharField(max_length = 32, blank = True)
    patch_file   = models.CharField(max_length = 100, blank = True)
    patch_md5    = models.CharField(max_length = 32, blank = True)
    create_time  = models.DateTimeField(default=datetime.now())
    pub_time     = models.DateTimeField(null = True, blank = True)
    is_tongji    = models.IntegerField()
    is_publish   = models.BooleanField(verbose_name=_(u'是否灰度发布版本'))
    class Meta:
        db_table = 'kx_pub'
        verbose_name_plural = verbose_name = _(u'灰度发布')
    def __unicode__(self):
        return unicode(self.ver)
        
class PublishUser(models.Model):
    email = models.EmailField(verbose_name=_(u'邮件地址'), max_length=50, unique=True)
    ver = models.ForeignKey(KxPub,db_column='ver')
    is_publish = models.BooleanField(verbose_name=_(u'是否灰度发布用户'))
    class Meta:
        db_table = 'publish_user'
        verbose_name_plural = verbose_name = _(u'灰度发布用户')
    def __unicode__(self):
        return unicode(self.ver)
