#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.db import models

class KxSoftBug(models.Model):
    id               = models.IntegerField(primary_key = True)
    client_identifie = models.CharField(max_length     = 32L)
    version          = models.CharField(max_length     = 10L)
    upload_time      = models.DateTimeField()
    os               = models.CharField(max_length     = 50L)
    auto_start       = models.IntegerField()
    lan_num          = models.IntegerField()
    u_email          = models.CharField(max_length     = 50L, blank = True)
    class Meta:
        db_table = 'kx_soft_bug'

