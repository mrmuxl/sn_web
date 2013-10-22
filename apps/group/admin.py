#_*_coding:utf-8_*_

from django.contrib import admin
from django.conf import settings
from models import Groups,GroupUser,GroupUserVerify,GroupPrintAuth
from models import GroupPrint,GroupManager

class GroupsAdmin(admin.ModelAdmin):
    pass

class GroupUserAdmin(admin.ModelAdmin):
    pass

class GroupUserVerifyAdmin(admin.ModelAdmin):
    pass

class GroupPrintAuthAdmin(admin.ModelAdmin):
    pass

class GroupPrintAdmin(admin.ModelAdmin):
    pass

class GroupManagerAdmin(admin.ModelAdmin):
    pass

if settings.DEBUG:
    admin.site.register(Groups,GroupsAdmin)
    admin.site.register(GroupUser,GroupUserAdmin)
    admin.site.register(GroupUserVerify,GroupUserVerifyAdmin)
    admin.site.register(GroupPrintAuth,GroupPrintAuthAdmin)
    admin.site.register(GroupPrint,GroupPrintAdmin)
    admin.site.register(GroupManager,GroupManagerAdmin)
