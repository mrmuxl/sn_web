#_*_coding:utf-8_*_

from django.contrib import admin
from django.conf import settings
from django.db.models import Max
from models import Groups,GroupUser,GroupUserVerify,PrintAuth
from models import GroupPrint,GroupManager


class GroupsAdmin(admin.ModelAdmin):
    list_display =('id','name','owner_id','user_num','max_num','g_type','create_time')
    def save_model(self,request,obj,forum,change):
        obj.creater_id =request.user
        if obj.g_type == 1:#普通群
            r = Groups.objects.filter(id__gte=20000).aggregate(max_id=Max('id'))
            if r['max_id'] == None:
                obj.pk = 20000
            else:
               obj.pk = r['max_id'] +1 
        elif obj.g_type == 2:#高校群
            r = Groups.objects.filter(id__gte=10001).filter(id__lte=19999).aggregate(max_id=Max('id'))
            if r['max_id'] == None:
                obj.pk = 10001
            else:
               obj.pk = r['max_id'] +1 
        obj.save()


class GroupUserAdmin(admin.ModelAdmin):
    list_display =('user_id','user_remark','share_print','join_time','joiner_id')
    def save_model(self,request,obj,forum,change):
        obj.joiner_id =request.user
        obj.save()
   

class GroupUserVerifyAdmin(admin.ModelAdmin):
    pass

class PrintAuthAdmin(admin.ModelAdmin):
    pass

class GroupPrintAdmin(admin.ModelAdmin):
    pass

class GroupManagerAdmin(admin.ModelAdmin):
    pass

if settings.DEBUG:
    admin.site.register(Groups,GroupsAdmin)
    admin.site.register(GroupUser,GroupUserAdmin)
#    admin.site.register(GroupUserVerify,GroupUserVerifyAdmin)
#    admin.site.register(GroupPrintAuth,GroupPrintAuthAdmin)
#    admin.site.register(GroupPrint,GroupPrintAdmin)
#    admin.site.register(GroupManager,GroupManagerAdmin)
