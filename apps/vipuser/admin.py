#_*_coding:utf-8_*_

from django.contrib import admin
from models import VIPUser
from models import Print,Shared,PrintAccess,SharedAccess

class VIPUserAdmin(admin.ModelAdmin):
    list_display = ('email','is_vip','expire')
    search_fields = ['email__email',]

#class AccessVIPUserAdmin(admin.ModelAdmin):
#    list_display = ('email','is_print','print_num','used_print_num','is_shared','shared_num','used_shared_num','expire')
#    search_fields = ['email__email',]
#class AccessUserAdmin(admin.ModelAdmin):
#    list_display = ('email','access_user')
#    search_fields = ['email__email',]
class PrintAdmin(admin.ModelAdmin):
    pass

class SharedAdmin(admin.ModelAdmin):
    pass

class PrintAccessAdmin(admin.ModelAdmin):
    pass

class SharedAccessAdmin(admin.ModelAdmin):
    pass

admin.site.register(VIPUser,VIPUserAdmin)
admin.site.register(Print,PrintAdmin)
admin.site.register(Shared,SharedAdmin)
admin.site.register(PrintAccess,PrintAccessAdmin)
admin.site.register(SharedAccess,SharedAccessAdmin)
