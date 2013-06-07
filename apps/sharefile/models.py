from django.db import models
from apps.kx.models import KxUser
from rest_framework import serializers

# Create your models here.

class ShareFile(models.Model):
    #owner = models.ForeignKey(KxUser, to_field='email', db_column='ower_email')
    fileName = models.CharField(max_length=80, db_column='share_name')
    size = models.IntegerField()
    cmtNum = models.IntegerField(db_column='comment_count')
    type = models.IntegerField(db_column='share_file_type')
    mac = models.CharField(max_length=100, db_column='owner_mac')
    ownerEmail = models.CharField(max_length=50, db_column='owner_email')
    ownerNick = models.CharField(max_length=20, db_column='nick')    

    class Meta:
        db_table = 'kx_share'

class ShareFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareFile
        fields = ('id', 'fileName', 'size', 'cmtNum', 'mac', 'type',
                'ownerEmail', 'ownerNick')
