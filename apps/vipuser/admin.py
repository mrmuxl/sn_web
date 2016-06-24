#_*_coding:utf-8_*_

from django.contrib import admin
from models import VIPUser

class VIPUserAdmin(admin.ModelAdmin):
    list_display = ('email_email','is_vip','expire')
    #fieldsets = (
    #    (u'用户基本信息', {'fields': ('email', 'is_vip','expire')}),
    #)
    def email_email(self, instance):
        return instance.email.email

admin.site.register(VIPUser,VIPUserAdmin)
