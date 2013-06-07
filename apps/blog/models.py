#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from apps.kx.models import KxUser


class KxForumForum(models.Model):
    id          = models.AutoField(primary_key = True)
    name        = models.CharField(_(u'分类名称'),max_length = 20L)
    posts_num   = models.IntegerField(default=0)
    order_num   = models.IntegerField(default=0)
    updater_id  = models.CharField(max_length=32L)
    update_time = models.DateTimeField()
    class Meta:
        db_table = 'kx_forum_forum'
        verbose_name_plural = verbose_name = _(u'文章分类')

class KxForumMpost(models.Model):
    id          = models.AutoField(primary_key = True)
    forum_id    = models.IntegerField(_(u'发布类别'))
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

class KxForumPosts(models.Model):
    id          = models.AutoField(primary_key = True)
    forum_id    = models.IntegerField(_(u'发布类别'))
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


BLOG_CHOICES = (
    (0,_(u'已发布')),
    (1,_(u'隐藏')),
    )
TOP_CHOICES = (
    (0,_(u'未置顶')),
    (1,_(u'已置顶')),
    )
class Blog(models.Model):
    id = models.AutoField(primary_key = True)
    author = models.ForeignKey(KxUser, editable=False)
    title = models.CharField(max_length = 100L)
    summary = models.TextField(verbose_name=_(u'摘要'))
    content= models.TextField(verbose_name=_(u'正文'))
    status  = models.IntegerField(verbose_name=_(u'文章状态'),default = 0,choices=BLOG_CHOICES,help_text=_(u'0=已发布，1=隐藏'))
    is_top =  models.BooleanField(verbose_name=_(u'置顶'),default = 0,choices=TOP_CHOICES,help_text=_(u'0=未置顶，1=已置顶'))
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'发布日期')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name=u'更新日期')
    class Meta:
        db_table = 'blog'
        verbose_name_plural = verbose_name = _(u'Blog')
 
