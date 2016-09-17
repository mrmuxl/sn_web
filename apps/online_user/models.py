from django.db import models
from rest_framework import serializers

# Create your models here.

class OnlineUser(models.Model):
    #owner = models.ForeignKey(KxUser, to_field='email', db_column='ower_email')
    mac = models.CharField(max_length=100, primary_key=True)
    email = models.CharField(max_length=50)
    #nick = models.CharField(max_length=20, db_column='nick')    
    lan_ip = models.CharField(max_length=50)
    wlan_ip = models.CharField(max_length=50)
    class Meta:
        db_table = 'kx_userlogin'

    def __unicode__(self):
        return self.mac


class OnlineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineUser 
        fields = ('mac',   'lan_ip', 'wlan_ip', 'email')
