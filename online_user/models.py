from django.db import models
from rest_framework import serializers

# Create your models here.

class OnlineUser(models.Model):
    #owner = models.ForeignKey(KxUser, to_field='email', db_column='ower_email')
    #mac = models.CharField(max_length=100, db_column='owner_mac')
    email = models.CharField(max_length=50, db_column='owner_email')
    #nick = models.CharField(max_length=20, db_column='nick')    
    lan_ip = models.CharField(max_length=50, blank=True)
    wlan_ip = models.CharField(max_length=50, blank=True)


class OnlineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineUser 
        fields = ('id', 'email',  'lan_ip', 'wlan_ip')
