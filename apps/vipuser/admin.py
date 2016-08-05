#_*_coding:utf-8_*_

from django.contrib import admin
from models import VIPUser

class VIPUserAdmin(admin.ModelAdmin):
    list_display = ('Email','is_vip','expire')
    search_fields = ['email__email',]
    #fieldsets = (
    #    (u'用户基本信息', {'fields': ('email', 'is_vip','expire')}),
    #)
    def Email(self, instance):
        return instance.email.email
    Email.short_description = u'邮箱'

admin.site.register(VIPUser,VIPUserAdmin)
