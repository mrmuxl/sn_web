#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from apps.kx.models import KxUser
from datetime import datetime

class VIPUser(models.Model):
    email = models.OneToOneField(KxUser,to_field='email',db_column='email',related_name='kxuser_email',verbose_name = _(u'邮箱'))
    is_vip = models.BooleanField(verbose_name=_(u'是否vip用户'))
    expire = models.DateTimeField(default = datetime.now(),verbose_name = _(u'过期时间'))
    class Meta:
        db_table = 'vipuser'
        verbose_name_plural = verbose_name = _(u'VIP用户')
