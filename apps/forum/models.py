#_*_coding:utf-8_*_

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from apps.kx.models import KxUser
from datetime import datetime

class ForumTags(models.Model):
    '''标签'''
    name = models.CharField(max_length=200, unique=True, verbose_name=u'名称')
    count_post = models.IntegerField(default=0, editable=False, verbose_name=u'文章数')
    class Meta:
        db_table = 'forum_tags'
        verbose_name_plural = verbose_name = u'标签'
    def __unicode__(self):
        return self.name

class ForumCategory(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    order = models.IntegerField(blank=True, null=True, verbose_name='顺序')
    class Meta:
        db_table = 'forum_category'
        verbose_name_plural = verbose_name = _(u'Forum分类')
        ordering = ['order',]
    def __unicode__(self):
        return self.name


STATUS_CHOICES = (
    (0,_(u'已发布')),
    (1,_(u'隐藏')),
    )

class ForumPost(models.Model):
    id  = models.AutoField(primary_key = True)
    #pid = models.ForeignKey("self",blank=True,null=True)
    category = models.ForeignKey(ForumCategory, verbose_name='分类')
    author = models.ForeignKey(KxUser, editable=False,verbose_name=_(u'作者'))
    vote_up = models.IntegerField(default=0, editable=True, verbose_name='赞成票')
    vote_down = models.IntegerField(default=0, editable=True, verbose_name='反对票')
    #slug = models.CharField(max_length=50, unique=True, db_index=True, verbose_name=u'Slug', help_text=u'页面的 URL 名称。可包含字母、数字、减号、下划线，不能是以下>    词语之一：archives、post、tag')
    tags = models.ManyToManyField(ForumTags, blank=True, verbose_name=u'标签')
    #summary = models.TextField(verbose_name=_(u'摘要'))
    title = models.CharField(max_length=200,verbose_name='标题')
    content= models.TextField(verbose_name=_(u'正文'))
    status  = models.IntegerField(verbose_name=_(u'文章状态'),default = 0,choices=STATUS_CHOICES,help_text=_(u'0=已发布，1=隐藏'))
    #is_above =  models.BooleanField(verbose_name=_(u'置顶'),default = 0,choices=TOP_CHOICES,help_text=_(u'0=未置顶，1=已置顶'))
    created = models.DateTimeField(default=datetime.now(), verbose_name='创建时间')
    modified = models.DateTimeField(default=datetime.now(), verbose_name='修改时间')
    hits = models.IntegerField(default=0, editable=False, verbose_name='点击次数')
    order = models.IntegerField(verbose_name = _(u'排序'),default = 0)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u'/forums/post/%d/' % (self.id)

    class Meta:
        db_table = 'forum_post'
        verbose_name_plural = verbose_name = _(u'Forum')
        ordering = ['-created',]
 

class ForumComment(models.Model):
    id  = models.AutoField(primary_key = True)
    fid = models.ForeignKey(ForumPost, verbose_name=_('Forum'))
    author = models.ForeignKey(KxUser, editable=False,verbose_name=_(u'作者'))
    content= models.TextField(verbose_name=_(u'正文'))
    ip = models.IPAddressField(null=True, blank=True, verbose_name=_('IP地址'))
    visible = models.BooleanField(default=True, verbose_name=_('是否可见'))
    created = models.DateTimeField(default=datetime.now(), verbose_name=_(u'创建时间'))

    class Meta:
        db_table = 'forum_comment'
        verbose_name_plural = verbose_name = _(u'回复')
        ordering = ['-created',]

    def __unicode__(self):
        return unicode(self.id)
