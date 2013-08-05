#_*_coding:utf-8_*_

from django.db import models
from apps.kx.models import KxUser
from rest_framework import serializers


# Create your models here.
class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = KxUser
        fields = ('id', 'email', 'nick', 'avatar', 'status', 'login_status')