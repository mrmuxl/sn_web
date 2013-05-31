#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


class KxForumForum(models.Model):
    id          = models.AutoField(primary_key = True)
    name        = models.CharField(_(u'分类名称'),max_length = 20L)
    posts_num   = models.IntegerField(default=0)
    order_num   = models.IntegerField(default=0)
    updater_id  = models.CharField(max_length=32L)
    update_time = models.DateTimeField()
    class Meta:
        db_table = 'kx_forum_forum'
        verbose_name_plural = verbose_name = _(u'文章类别')

class KxForumMpost(models.Model):
    id          = models.AutoField(primary_key = True)
    forum_id    = models.IntegerField(_(u'发布类别'),default=1)
    title       = models.CharField(max_length = 100L)
    user_id     = models.CharField(max_length=32L)
    reply_num   = models.IntegerField()
    view_num    = models.IntegerField()
    top_num     = models.IntegerField()
    is_fine     = models.IntegerField()
    attach      = models.IntegerField()
    posts_type  = models.IntegerField()
    is_del      = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    last_time   = models.DateTimeField()
    last_uid    = models.IntegerField()
    class Meta:
        db_table = 'kx_forum_mpost'
        verbose_name = _(u'Mpost')
        verbose_name_plural = _(u'MPost')

#FORUM_CHOICES = (
#    
#)

class KxForumPosts(models.Model):
    id          = models.AutoField(primary_key = True)
    forum_id    = models.IntegerField(_(u'发布类别'),default=1)
    tid         = models.IntegerField()
    title       = models.CharField(max_length = 100L)
    content     = models.TextField()
    user_id     = models.CharField(max_length=32L)
    reply_id    = models.IntegerField()
    is_main     = models.IntegerField()
    user_ip     = models.CharField(max_length = 15L)
    is_del      = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    class Meta:
        db_table = 'kx_forum_posts'
        verbose_name_plural = verbose_name = _(u'文章')

