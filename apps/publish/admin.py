#_*_coding:utf-8_*_

from django.contrib import admin
from models import PublishUser,KxPub
from forms import PublishUserForm

class PublishUserAdmin(admin.ModelAdmin):
    publish_user = PublishUserForm
    list_filter = ('is_publish',)
    list_display =('email','ver','repo_ver')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (u'添加用户', {
            'classes': ('wide',),
            'fields': ('email', 'ver', 'repo_ver')}
        ),
    )

admin.site.register(PublishUser,PublishUserAdmin)
