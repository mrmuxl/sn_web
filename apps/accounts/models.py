#_*_coding:utf-8_*_
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.conf import settings


# 用户验证问题（提问）
class UserAuthIssue(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=32,unique=True)
    is_auth = models.BooleanField(default=0)
    issue = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_auth_issue'
