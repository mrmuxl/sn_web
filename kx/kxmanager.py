#_*_coding:utf-8_*_

from django.contrib.auth.models import (BaseUserManager)
from django.utils import timezone
from django.db import models

class KxUserManager(BaseUserManager):
    def create_user(self,email,username,password=None,**extra_fields):
        """
        创建一个用户，用户名是email，和密码
        """
        if not email:
            raise ValueError(u'用户名必须是email地址')
        user = self.model(email=email,username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,**extra_fields):
        """
        创建一个超级用户
        """
        u = self.create_user(email=email,password=password,username=username,**extra_fields)
        u.is_staff = True
        u.is_admin = True
        u.is_superuser = True
        u.save(using=self._db)
        return u
