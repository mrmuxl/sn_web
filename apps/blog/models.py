#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from apps.kx.models import KxUser
from datetime import datetime


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

class Category(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    slug = models.SlugField()
    order = models.IntegerField(blank=True, null=True, verbose_name='顺序')
    class Meta:
        db_table = 'category'
        verbose_name_plural = verbose_name = _(u'博客分类')
        ordering = ['order',]
    def __unicode__(self):
        return self.name


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
    category = models.ForeignKey(Category, verbose_name='分类')
    author = models.ForeignKey(KxUser, editable=False,verbose_name=_(u'作者'))
    title = models.CharField(max_length = 100L,verbose_name=_(u'标题'))
    slug = models.CharField(max_length=50, unique=True, db_index=True, verbose_name=u'Slug', help_text=u'页面的 URL 名称。可包含字母、数字、减号、下划线，不能是以下>    词语之一：archives、post、tag')
    summary = models.TextField(verbose_name=_(u'摘要'))
    content= models.TextField(verbose_name=_(u'正文'))
    status  = models.IntegerField(verbose_name=_(u'文章状态'),default = 0,choices=BLOG_CHOICES,help_text=_(u'0=已发布，1=隐藏'))
    is_above =  models.BooleanField(verbose_name=_(u'置顶'),default = 0,choices=TOP_CHOICES,help_text=_(u'0=未置顶，1=已置顶'))
    created = models.DateTimeField(default=datetime.now(), verbose_name='创建时间')
    modified = models.DateTimeField(default=datetime.now(), verbose_name='修改时间')
    hits = models.IntegerField(default=0, editable=False, verbose_name='点击次数')
    class Meta:
        db_table = 'blog'
        verbose_name_plural = verbose_name = _(u'博客')
        ordering = ['-is_above', '-created']
 
    def __unicode__(self):
        return self.title
