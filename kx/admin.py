#_*_coding:utf-8_*_

#from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm

from kx.models import KxUser
from kx.admin_forms import (UserChangeForm,UserCreationForm)

class KxUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','nick','last_login')
    list_filter = ('is_staff','is_superuser','status')
    fieldsets = (
        (u'用户基本信息', {'fields': ('email', 'password')}),
        (u'用户详细信息', {'fields': ('nick','status','active_time')}),
        (u'用户登陆时间', {'fields': ('last_login','create_time',)}),
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

# Now register the new UserAdmin...
admin.site.register(KxUser, KxUserAdmin)
# ... and, since we're not using Django's builtin permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
