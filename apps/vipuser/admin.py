#_*_coding:utf-8_*_

from django.contrib import admin
from models import VIPUser
from models import Print,Shared,PrintAccess,SharedAccess

class VIPUserAdmin(admin.ModelAdmin):
    list_display = ('email','is_vip','create_at','expire')
    search_fields = ['email__email',]

class PrintAdmin(admin.ModelAdmin):
    list_display = ('email','is_print','print_num','used_print_num','create_at','expire')
    search_fields = ['email__email',]

class SharedAdmin(admin.ModelAdmin):
    list_display = ('email','is_shared','shared_num','used_shared_num','create_at','expire')
    search_fields = ['email__email',]

class PrintAccessAdmin(admin.ModelAdmin):
    list_display = ('email','access_user','create_at','status')
    search_fields = ['email__email__email',]

class SharedAccessAdmin(admin.ModelAdmin):
    list_display = ('email','access_user','create_at','status')
    search_fields = ['email__email__email',]

admin.site.register(VIPUser,VIPUserAdmin)
admin.site.register(Print,PrintAdmin)
admin.site.register(Shared,SharedAdmin)
admin.site.register(PrintAccess,PrintAccessAdmin)
admin.site.register(SharedAccess,SharedAccessAdmin)
