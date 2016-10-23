#_*_coding:utf-8_*_

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm

from apps.kx.models import KxUser
from apps.kx.forms import (UserChangeForm,UserCreationForm)
from apps.vipuser.models import VIPUser
from apps.publish.models import PublishUser
from apps.ad.admin import OperatorInline

class VIPUserInline(admin.StackedInline):
    fk_name = 'email'
    model = VIPUser
    #fieldsets=(
    #    (None, {
    #        'fields': ('is_vip', 'expire')
    #    }),
    #)

class KxUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = [VIPUserInline,OperatorInline]

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','nick','create_time','last_login')
    list_filter = ('is_staff','is_superuser','status')
    fieldsets = (
        (u'用户基本信息', {'fields': ('email', 'password')}),
        (u'用户详细信息', {'fields': ('nick','status')}),
        (u'用户登陆时间', {'fields': ('active_time','last_login','create_time',)}),
    )
    add_fieldsets = (
        (u'添加用户', {
            'classes': ('wide',),
            'fields': ('email', 'nick', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(KxUser, KxUserAdmin)
admin.site.unregister(Group)
